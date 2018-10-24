`timescale 10ps / 1ps
`celldefine
module boothEncoding(a, encoding, pp);

  input [6:0] a;
  input [2:0] encoding;
  output reg [8:0] pp;

  always @(a or encoding) begin
    case(encoding)
      3'b000: pp = 9'b0000_0000_0;
      3'b001: pp = {{2{a[6]}},a}; // sign extend
      3'b010: pp = {{2{a[6]}},a}; //sign extend
      3'b011: pp = {a[6],a,1'b0}; // mult 2 and sign extend
      3'b100: pp = {~{a[6],a},1'b1} + 1'b1; //mult 2, twos comp, sign extend
      3'b101: pp = {~{2{a[6]}},~a} + 1'b1;
      3'b110: pp = {~{2{a[6]}},~a} + 1'b1;
      3'b111: pp = 9'b0000_0000_0;
    endcase
  end

endmodule
`endcelldefine
