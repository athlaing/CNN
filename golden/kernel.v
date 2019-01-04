module kernel
#(
  parameter b0 = 16'bxx,
  parameter b1 = 16'bxx,
  parameter b2 = 16'bxx,
  parameter b3 = 16'bxx,
  parameter b4 = 16'bxx,
  parameter b5 = 16'bxx,
  parameter b6 = 16'bxx,
  parameter b7 = 16'bxx,
  parameter b8 = 16'bxx
)
(clk, fifo_clk, data, reset);
reg [15:0] a0, a1, a2, a3, a4, a5, a6, a7, a8;
wire [15:0] out0, out1, out2, out3, out4, out5, out6, out7, out8;
reg state_c, state;

reg [47:0] fifo_out;

parameter EVEN = 1'b0;
parameter ODD = 1'b1;

/*
|---|---|---|
| 0 | 3 | 6 |
|---|---|---|
| 1 | 4 | 7 |
|---|---|---|
| 2 | 5 | 8 |
|---|---|---|
*/

syn_fifo(.clk(fifo_clk), data_in, .data_out, read_en, write_en, .reset(reset));

bfloat_mult16 ind0(.clk(clk), .a(a0), .b(b0), .out(out0));
bfloat_mult16 ind1(.clk(clk), .a(a1), .b(b1), .out(out1));
bfloat_mult16 ind2(.clk(clk), .a(a2), .b(b2), .out(out2));
bfloat_mult16 ind3(.clk(clk), .a(a3), .b(b3), .out(out3));
bfloat_mult16 ind4(.clk(clk), .a(a4), .b(b4), .out(out4));
bfloat_mult16 ind5(.clk(clk), .a(a5), .b(b5), .out(out5));
bfloat_mult16 ind6(.clk(clk), .a(a6), .b(b6), .out(out6));
bfloat_mult16 ind7(.clk(clk), .a(a7), .b(b7), .out(out7));
bfloat_mult16 ind8(.clk(clk), .a(a8), .b(b8), .out(out8));

always @(posedge fifo_clk) begin
  // read and write in some ratio
end

always @(posedge clk) begin
  if(reset) begin
    state <= ODD;
  end
  else begin
    case(state)
      ODD: begin
        a0 <= fifo_out[15:0];
        a1 <= fifo_out[31:16];
        a2 <= fifo_out[47:32];
        a6 <= a0;
        a7 <= a1;
        a8 <= a2;
        state <= ODD;
      end
      EVEN: begin
        a3 <= fifo_out[15:0];
        a4 <= fifo_out[31:16];
        a5 <= fifo_out[47:32];
        state <= EVEN;
      end
    endcase
  end
end
endmodule
