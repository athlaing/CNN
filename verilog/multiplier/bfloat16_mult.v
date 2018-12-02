module bfloat16_mult(clk, a, b, out);
  input clk;
  input [15:0] a, b;
  output reg [15:0] out;

  reg  [15:0] a_r, b_r;
  wire [8:0]  a_e, b_e;
  reg  [9:0]  a_e_r, b_e_r;


  wire s0, s1, s2, s3, s4;
  reg  s0_r, s1_r, s2_r, s3_r, s4_r;

  wire [8:0] e1, e2, e3;
  reg  [8:0] e1_r;
  reg  [8:0] e2_r;
  reg  [8:0] e3_r;

  wire [15:0] man16;
  reg  [3:0]  shift;

  wire [15:0] man;
  wire [8:0]  exp;
  wire        sign;



   always @(man16) begin
        casez(man16)
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
        endcase // for getting rid of leading 1s/0s
     end
   bfloat_mantissa_mult m0(.clk(clk), .a({2'b01,a_r[6:0]}), .b({2'b01,b_r[6:0]}), .out(man16));

    //clock 0
    assign a_e = {1'b0, a_r[14:7]} + 9'b110000001; // -127
    assign b_e = {1'b0, b_r[14:7]} + 9'b110000001; // -127
    assign s0 = a[15] ^ b[15];

    //clock 1
    assign e1 = a_e_r + b_e_r;
    assign s1 = s0_r;

    //clock 2
    assign e2 = e1_r + 9'b010000000; // +128
    assign s2 = s1_r;

    //clock 3
    assign e3 = e2_r;
    assign s3 = s2_r;

    //clock 4
    assign man = man16 << shift;
    assign exp = ~({5'b00000,shift}) + 1'b1 + e3_r; // exp is a negative of the shift
    assign s4 = s3_r;

    //clock 5
    assign sign = s4_r;

   always @(posedge clk) begin
    a_r       <= a;
    b_r       <= b;
    a_e_r     <= a_e;
    b_e_r     <= b_e;
    e1_r      <= e1;
    e2_r      <= e2;
    e3_r      <= e3;
    s0_r      <= s0;
    s1_r      <= s1;
    s2_r      <= s2;
    s3_r      <= s3;
    s4_r      <= s4;
    out[15]   <= sign;
    out[14:7] <= exp[7:0];
    out[6:0]  <= man[14:8];
  end
 endmodule
