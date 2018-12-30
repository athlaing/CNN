
/******************************************************************************
 * module reads bits from TDI
 *****************************************************************************/
 
 module Receiver (	TDI,
							TCS,
							TCK,
							data,
							done);
	input TDI; // data loaded into TDI
	input TCS; // chip select high when data is coming
	input TCK; // clock
	output reg done; // data is read for reading
	output reg [7:0] data; // data stored from one transcation
	reg [2:0] cycle; // data comes in bytes
	
	
	always @ (posedge TCK or posedge TCS) begin
		if(TCS) begin
			done <= 0;
			cycle <= 0;
		end // while cs is high
		else begin
			cycle <= cycle + 1;
			data <= {TDI , data[7:1]};
			if(cycle == 0) begin
				data <= {TDI, data[7:1]};
				done <= 1;
			end // counter overflows read complete
			else begin
				done <= 0;
			end //done not ready
		end // low 
	end // clock data in when cs is high	
	
endmodule // receiver

/******************************************************************************
 * module reads bits from TDO
 *****************************************************************************/
module Transmitter (		TDO,
								TCS,
								TCK,
								data,
								done);
	
	input TCS; // chip select high when data is coming
	input TCK; // clock
	input [7:0] data; // data stored from one transcation
	
	output reg TDO; // data loaded into TDI
	output reg done; // data is read for reading
	
	reg [2:0] cycle; // data comes in bytes
	
	
	always @ (posedge TCK or posedge TCS) begin
		if(TCS) begin
			done <= 0;
			cycle <= 0;
			TDO <= 0;
		end // while cs is high
		else begin
			cycle <= cycle + 1;
			TDO <= data[cycle];
			if(cycle == 7) begin
				done <= 1;
			end // complete
			else begin
				done <= 0;
			end // not ready
		end // low 
	end // clock data in when cs is high
	
endmodule // transmitter