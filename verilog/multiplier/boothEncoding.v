//`timescale 10ps / 1ps
//`celldefine
module boothEncoding(a, encoding, pp);

  input [6:0] a;
  input [2:0] encoding;
  output reg [9:0] pp;

  always @(a or encoding) begin
    case(encoding)
      3'b000: pp = 10'b0000_0000_00;
      3'b001: pp = {3'b000, a};
      3'b010: pp = {3'b000, a};
      3'b011: pp = {2'b00, a, 1'b0};
      3'b100: pp = ~{2'b00, a, 1'b0} + 1'b1;
      3'b101: pp = ~{3'b000, a} + 1'b1;
      3'b110: pp = ~{3'b000, a} + 1'b1;
      3'b111: pp = 10'b0000_0000_00;
    endcase
  end

endmodule
//`endcelldefine
