module bfloat16_mult(clk, a, b, out);
  input clk;
  input [15:0] a, b;
  output reg [15:0] out;
  
  reg  [15:0] a_r, b_r;
  wire [8:0]  a_e, b_e;
  reg  [9:0]  a_e_r, b_e_r;
  

  wire s0, s1, s2;
  reg  s0_r, s1_r, s2_r;
  
  wire [8:0] e1, e2;
  reg  [8:0] e1_r;
  reg  [7:0] e2_r;
  
  wire [13:0] man14;
  reg  [3:0]  shift;
  
  wire [13:0] man;
  wire [7:0] exp;
  wire       sign;
  
  
   always @(man14) begin
        casez(man14)
            14'b1?????????????: shift = 4'b0000;
            14'b01????????????: shift = 4'b0001;
            14'b001???????????: shift = 4'b0010;
            14'b0001??????????: shift = 4'b0011;
            14'b00001?????????: shift = 4'b0100;
            14'b000001????????: shift = 4'b0101;
            14'b0000001???????: shift = 4'b0110;
            14'b00000001??????: shift = 4'b0111;
            14'b000000001?????: shift = 4'b1000;
            14'b0000000001????: shift = 4'b1001;
            14'b00000000001???: shift = 4'b1010;
            14'b000000000001??: shift = 4'b1011;
            14'b0000000000001?: shift = 4'b1100;
            14'b00000000000001: shift = 4'b1101;
            default: shift = 4'b0000;
        endcase // for getting rid of leading 1s/0s
     end
   bfloat_mantissa_mult m0(.clk(clk), .a(a[6:0]), .b(b[6:0]), .out(man14));
    
    //clock 0 
    assign a_e = {1'b0, a_r[14:7]} + 9'b110000001; // -127
    assign b_e = {1'b0, b_r[14:7]} + 9'b110000001; // -127
    assign s0 = a[15] ^ b[15];
   
    //clock 1 
    assign e1 = a_e_r + b_e_r;
    assign s1 = s0_r;
    
    //clock 2
    assign e2 = e1_r + 9'b0011_1111_1; // +127
    assign s2 = s1_r;
    
    //clock 3
    assign man = man14 << shift;
    assign exp = ~(shift) + e2_r; // exp is a negative of the shift
    assign sign= s2_r;
    
   always @(posedge clk) begin
    a_r       <= a;
    b_r       <= b;
    a_e_r     <= a_e;
    b_e_r     <= b_e;
    e1_r      <= e1;
    e2_r      <= e2[7:0];
    s0_r      <= s0;
    s1_r      <= s1;
    s2_r      <= s2;
    out[15]   <= sign;
    out[14:7] <= exp;
    out[6:0]  <= man[13:7];
  end
 endmodule