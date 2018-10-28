module bfloat16_mult(clk, a, b, out);
  input clk;
  input [15:0] a, b;
  output reg [15:0] out;
  reg [15:0] a_r, b_r;
  wire [9:0] a_e, b_e;
  reg [9:0] a_e_r, b_e_r;
  wire [10:0] out_e;
  reg [10:0] out_e_r;
  wire out_s0, out_s1, out_s2;
  reg out_s0_r, out_s1_r;


  always @(in) begin
        casez(in)
            7'b01?????: shift = 4'b000;
            7'b001????: shift = 4'b001;
            7'b0001???: shift = 4'b010;
            7'b00001??: shift = 4'b011;
            7'b0000010: shift = 4'b100;
            7'b0000001: shift = 4'b101;
            7'b0000000: shift =
            default: shift = 4'b000;
        endcase // for getting rid of leading 1s/0s

    man = in << shift;
    mantissa = man[6:3]; // take 4 bits for 3.1 notation
    exp = ~(shift) + 4'b0001; // exp is a negative of the shift

    end

  bfloat_mantissa_mult m0(.clk(clk), .a(a[6:0]), .b(b[6:0]), .out(out[13:]));

  assign a_e = {1'b0, a_r[30:23]} + 9'b110000001 // -127
  assign b_e = {1'b0, b_r[30:23]} + 9'b110000001 // -127
  assign out_s0 = a[31] ^ b[31];

  assign out_e = a_e_r + b_e_r;
  assign out_s1 = out_s0_r;

  assign out_e_bias = out_e_r + 9'b0011_1111_1;
  assign out_s2;

  always @(posedge clk) begin
    a_r <= a;
    b_r <= b;
    a_e_r <= a_e;
    b_e_r <= b_e;
    out_e_r <= out_e;
    out[30:23] <= out_e_bias[7:0];
    out_s0_r <= out_s0;
    out_s1_r <= out_s1;
    out[31] <= out_s2;
  end

endmodule
