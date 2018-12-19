module bfloat16_add(reset, clk, a, b, out, ready);
  input reset, clk;
  input [15:0] a, b;
  output reg [15:0] out;
  reg [15:0] out_c;
  output reg ready;
  reg ready_c;
  reg [15:0] input_a, input_b;
  reg [15:0] a_r, b_r;
  reg a_s_c, b_s_c, a_s, b_s, out_s_c, out_s;
  reg [7:0] a_m_c, b_m_c, a_m, b_m, out_m_c, out_m, out_e, out_e_c;
  reg [9:0] a_e_c, b_e_c, a_e, b_e, diff_e, neg_diff_e;
  reg [8:0] result_c, result;
  reg [2:0] state, state_c;

  reg [9:0] holder;

  parameter INIT      = 3'b000;
  parameter DECODE    = 3'b001;
  parameter CHECK     = 3'b010;
  parameter SHIFT     = 3'b011;
  parameter ADD       = 3'b100;
  parameter NORMALIZE = 3'b101;
  parameter RETURN    = 3'b110;

  always @(*) begin
    case(state)
    /*========================================================================*/
      INIT: begin
        input_a = a;
        input_b = b;
        state_c = DECODE;
      end
    /*========================================================================*/
      DECODE: begin
        a_s_c = a_r[15];
        b_s_c = b_r[15];
        a_m_c = {1'b0, a_r[6:0]};
        b_m_c = {1'b0, b_r[6:0]};
        a_e_c = {2'b00, a_r[14:7]} + 10'b1110000001;
        b_e_c = {2'b00, b_r[14:7]} + 10'b1110000001;
        state_c = CHECK;
      end
    /*========================================================================*/
      CHECK: begin
        // if infinity or NaN, return 16 ones
        if((a_e == 10'b0010000000) || (b_e == 10'b0010000000)) begin
          out_s_c = 1'b1;
          out_m_c = 8'b1111_1111;
          out_e_c = 8'b1111_1111;
          state_c = RETURN;
        end
        // if both a and b are 0, return 0
        else if((a_e == 10'b1110000001) && (b_e == 10'b1110000001) && (a_m == 0)
        && (b_m == 0)) begin
          out_s_c = 1'b0;
          out_m_c = 8'b0000_0000;
          out_e_c = 8'b0000_0000;
          state_c = RETURN;
        end
        // if a = 0 and b != 0, return b
        else if((a_e == 10'b1110000001) && (a_m == 0)) begin
          out_s_c = b_s;
          out_m_c = b_m;
          holder  = (b_e + 10'b0001111111);
          out_e_c = holder[7:0];
          state_c = RETURN;
        end
        // if b = 0 and a != 0, return a
        else if((b_e == 10'b1110000001) && (b_m == 0)) begin
          out_s_c = a_s;
          out_m_c = a_m;
          holder  = a_e + 10'b0001111111;
          out_e_c = holder[7:0];
          state_c = RETURN;
        end
        // if denormal number, change exponent to -126
        // else, add implicit leading one bit
        else begin
          if(b_e == 10'b1110000001) begin
            b_e_c = 10'b1110000010;
          end
          else begin
            b_m_c[7] = 1'b1;
          end
          if(a_e == 10'b1110000001) begin
            a_e_c = 10'b1110000010;
          end
          else begin
            a_m_c[7] = 1'b1;
          end
          state_c = SHIFT;
        end
      end
    /*========================================================================*/
      SHIFT: begin
        // not caring about rounding because this will be used in cnns
        diff_e = a_e + ~(b_e) + 10'b0000_0000_01;
        neg_diff_e = ~(diff_e) + 10'b0000_0000_01;
        // if a_e - b_e > 0, meaning a_e > b_e
        if(diff_e[9] == 1'b0) begin
          b_m_c = b_m >> diff_e;
          b_e_c = a_e;
        end
        // if a_e - b_e < 0, meaning a_e < b_e
        else if(diff_e[9] == 1'b1) begin
          a_m_c = a_m >> neg_diff_e;
          a_e_c = b_e;
        end
        state_c = ADD;
      end
    /*========================================================================*/
      ADD: begin
        holder = (a_e + 10'b000111_1111);
        out_e_c = holder[7:0];
        if(a_s == b_s) begin
          result_c = a_m + b_m;
          out_s_c = a_s;
        end
        else if((a_s == 1'b1) && (b_s == 1'b0)) begin
          if(a_m > b_m) begin
            result_c = a_m - b_m;
            out_s_c = 1'b1;
          end
          else begin
            result_c = b_m - a_m;
            out_s_c = 1'b0;
          end
        end
        else if ((b_s == 1'b1) && (a_s == 1'b0)) begin
          if(b_m > a_m) begin
            result_c = b_m - a_m;
            out_s_c = 1'b1;
          end
          else begin
            result_c = a_m - b_m;
            out_s_c = 1'b0;
          end
        end
        state_c = NORMALIZE;
      end
    /*========================================================================*/
      NORMALIZE: begin
        if((result_c[8:7] == 2'b11) || (result_c[8:7] == 2'b10)) begin
          out_m_c = result_c[8:2];
          out_e_c = out_e + 8'b0000_0010;
        end
        else if(result_c[8:7] == 2'b01) begin
          out_m_c = result_c[7:1];
          out_e_c = out_e + 8'b0000_0001;
        end
        else if(result_c[8:7] == 2'b00) begin
          out_m_c = result_c[6:0];
          out_e_c = out_e;
        end
        state_c = RETURN;
      end
    /*========================================================================*/
      RETURN: begin
        out_c[15] = out_s;
        out_c[14:7] = out_e;
        out_c[6:0] = out_m;
        ready_c = 1'b1;
        state_c = INIT;
      end
    endcase
    /*========================================================================*/
    if(reset) begin
      state_c = INIT;
    end
  end

  always @(posedge clk) begin
    state <= state_c;
    a_r <= input_a;
    b_r <= input_b;
    a_s <= a_s_c;
    b_s <= b_s_c;
    a_m <= a_m_c;
    b_m <= b_m_c;
    a_e <= a_e_c;
    b_e <= b_e_c;
    out_e <= out_e_c;
    out_m <= out_m_c;
    out_s <= out_s_c;
    ready <= ready_c;
    out <= out_c;
  end
endmodule
