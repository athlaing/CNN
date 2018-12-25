module booth_encoding(a, encoding, pp);
  input [8:0] a;
  input [2:0] encoding;
  output reg [9:0] pp;

  always @(a or encoding) begin
    case(encoding)
      3'b000: pp = 10'b0000_0000_00;       // 0
      3'b001: pp = {1'b0, a};              // a
      3'b010: pp = {1'b0, a};              // a
      3'b011: pp = {a, 1'b0};              // 2a
      3'b100: pp = ~{a, 1'b0} + 1'b1;      //-2a
      3'b101: pp = ~{1'b0, a} + 1'b1;      //-a
      3'b110: pp = ~{1'b0, a} + 1'b1;      //-a
      3'b111: pp = 10'b0000_0000_00;       // 0
    endcase
  end
endmodule
