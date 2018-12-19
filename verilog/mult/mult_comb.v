module bfloat16_mult(clk, a, b, out);
  input clk;
  input [15:0] a;
  input [15:0] b;
  input [15:0] out;
  wire [15:0] out_c;
  wire [15:0] man_mult_out;
  wire [15:0] man;
  reg [3:0] shift;
  wire [8:0] neg_shift;
  wire [8:0] exp;

  bfloat_man_mult m0(.a({2'b01, a_r[6:0]}), .b({2'b01, b_r[6:0]}), .out(man_mult_out));

  always @(man_mult_out) begin
    casez(man_mult_out)
      16'b1???????????????: shift = 4'd00;
      16'b01??????????????: shift = 4'd01;
      16'b001?????????????: shift = 4'd02;
      16'b0001????????????: shift = 4'd03;
      16'b00001???????????: shift = 4'd04;
      16'b000001??????????: shift = 4'd05;
      16'b0000001?????????: shift = 4'd06;
      16'b00000001????????: shift = 4'd07;
      16'b000000001???????: shift = 4'd08;
      16'b0000000001??????: shift = 4'd09;
      16'b00000000001?????: shift = 4'd10;
      16'b000000000001????: shift = 4'd11;
      16'b0000000000001???: shift = 4'd12;
      16'b00000000000001??: shift = 4'd13;
      16'b000000000000001?: shift = 4'd14;
      16'b0000000000000001: shift = 4'd15;
      default: shift = 4'd00;
    endcase
  end

  assign a_e = {1'b0, a_r[14:7]} + 9'b110000001; // -127
  assign b_e = {1'b0, b_r[14:7]} + 9'b110000001; // -127
  assign out_c[15] = a_r[15] ^ b_r[15];
  assign man = man_mult_out << shift;
  assign out_c[6:0] = man[14:8];
  assign neg_shift = ~({5'b00000, shift}) + 1;
  assign exp = a_e + b_e + 9'b010000000 + neg_shift;
  assign out_c[14:7] = exp[7:0];

  always @(posedge clk) begin
    a_r <= a;
    b_r <= b;
    out <= out_c;
  end
endmodule
