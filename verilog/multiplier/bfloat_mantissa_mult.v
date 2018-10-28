//`timescale 10ps/1ps
//`celldefine
module bfloat_mantissa_mult(clk, a, b, out);
  input [6:0] a;
  input [6:0] b;
  input clk;
  output reg [13:0] out;
  wire [13:0] out_c;
  wire [9:0] pp0_c, pp1_c, pp2_c, pp3_c;
  reg  [9:0] pp0, pp1, pp2, pp3;
  wire [13:0] row0, row1;
  reg  [13:0] row0_r, row1_r;
  wire cout0, cout1, cout2, cout3, cout4, cout5, cout6;
  wire dump0, dump1;
  reg [6:0] a_r, b_r;  
   
  boothEncoding b0(.a(a_r), .encoding({b_r[1:0],1'b0}), .pp(pp0_c));
  boothEncoding b1(.a(a_r), .encoding(b_r[3:1]), .pp(pp1_c));
  boothEncoding b2(.a(a_r), .encoding(b_r[5:3]), .pp(pp2_c));
  boothEncoding b3(.a(a_r), .encoding({1'b0, b_r[6:5]}), .pp(pp3_c));

  adder32 a32_0(.a(pp0[4]), .b(pp1[2]), .cin(pp2[0]), .cout(row0[5]), .sum(row0[4]));
  adder32 a32_1(.a(pp0[5]), .b(pp1[3]), .cin(pp2[1]), .cout(row0[6]), .sum(row1[5]));
  adder42 a42_0(.a(pp0[6]), .b(pp1[4]), .c(pp2[2]), .d(pp3[0]), .cin(1'b0), .carry(row0[7]), .sum(row1[6]), .cout(cout0));
  adder42 a42_1(.a(pp0[7]), .b(pp1[5]), .c(pp2[3]), .d(pp3[1]), .cin(cout0), .carry(row0[8]), .sum(row1[7]), .cout(cout1));
  adder42 a42_2(.a(pp0[8]), .b(pp1[6]), .c(pp2[4]), .d(pp3[2]), .cin(cout1), .carry(row0[9]), .sum(row1[8]), .cout(cout2));
  adder42 a42_3(.a(pp0[9]), .b(pp1[7]), .c(pp2[5]), .d(pp3[3]), .cin(cout2), .carry(row0[10]), .sum(row1[9]), .cout(cout3));
  adder42 a42_4(.a(pp0[9]), .b(pp1[8]), .c(pp2[6]), .d(pp3[4]), .cin(cout3), .carry(row0[11]), .sum(row1[10]), .cout(cout4));
  adder42 a42_5(.a(pp0[9]), .b(pp1[9]), .c(pp2[7]), .d(pp3[5]), .cin(cout4), .carry(row0[12]), .sum(row1[11]), .cout(cout5));
  adder42 a42_6(.a(pp0[9]), .b(pp1[9]), .c(pp2[8]), .d(pp3[6]), .cin(cout5), .carry(row0[13]), .sum(row1[12]), .cout(cout6));
  adder42 a42_7(.a(pp0[9]), .b(pp1[9]), .c(pp2[9]), .d(pp3[7]), .cin(cout6), .carry(dump0), .sum(row1[13]), .cout(dump1));

  assign row0[3:0] = pp0[3:0];
  assign row1[4:0] = {1'b0, pp1[1:0], 2'b00};

  assign out_c = row1_r + row0_r;

  always @(posedge clk) begin
    a_r <= a;
    b_r <= b;
    pp0 <= pp0_c;
    pp1 <= pp1_c;
    pp2 <= pp2_c;
    pp3 <= pp3_c;
    row1_r <= row1;
    row0_r <= row0;
    out <= out_c;
  end
endmodule
//`endcelldefine