`timescale 10ps/1ps
`celldefine
module adder32(a, b, c, cout, sum); 

	input a;
	input b;
	input c;
	output cout;
	output sum;

	assign sum = a ^ b ^ c;
	assign cout = (a & b) | (c & (a ^ b));

endmodule
`endcelldefine
