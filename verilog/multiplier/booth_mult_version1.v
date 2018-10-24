module booth(clk, resetN, start, multiplicand, multiplier, done, result);
	parameter n = 8;
	input clk, resetN, start;
	input [n-1:0] multiplicand, multiplier;
	output wire done;
	output wire [n+n-1:0] result;
	reg [n+1:0] A, C, acc; 
	reg [n:0] B;
	reg [n:0] shiftCount = 0;
	always @(posedge clk) begin if (~resetN || done) begin shiftCount <= 0;
		end else if (start && shiftCount == 0) begin A <= 0;
			B <= {multiplier, 1'b0};
			C <= {multiplicand[n-1],multiplicand[n-1],multiplicand};
		end else if (C == {multiplicand[n-1],multiplicand[n-1],multiplicand}) begin {A,B} <= {acc[n+1],acc[n+1],acc,B[n:2]};
			shiftCount <= shiftCount + 1;
		end end always @* begin if (B[2:0] == 3'b001 || B[2:0] == 3'b010) acc = A + C; 
		else if (B[2:0] == 3'b101 || B[2:0] == 3'b110) acc = A - C;
		else if (B[2:0] == 3'b011) acc = A + 2*C;
		else if (B[2:0] == 3'b100) acc = A - 2*C;
		else acc = A;
		end assign done = (shiftCount > (n/2)-1);
	assign result = {A[n-1:0],B[n:1]};	
endmodule
		