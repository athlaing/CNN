//`timescale 10ps/1ps
//`celldefine
module adder32(a, b, cin, cout, sum); 

	input a;
	input b;
	input cin;
	output cout;
	output sum;

	assign sum = a ^ b ^ cin;
	assign cout = (a & b) | (cin & (a ^ b));

endmodule
//`endcelldefine
