module Serializer(	// HOST lines
							inTCK, 	// input CLK
							inTCS,	// input chip slect
							inTDI, 	// input data from HOST comes in bytes
							// FPGA interfacing sigbnsla
							byteAddr,
							outputByte
						);
						
	input inTDI; // data loaded into TDI
	input inTCS; // chip select high when data is coming
	input inTCK; // clock
	output [7:0] byteAddr; // used to address the output reg
	output [7:0] outputByte;
	
	// variables for one trascction
	reg bytesRead_c[256]; 	// combinations bytesread
	reg bytesRead[256]; 		// max of 256 bytes send from host
	reg transaction[2048]; 	// holds all the data from transcation
	
	assign outputByte = transcation[byteAddr];
	
	// TCS operates active low
	// data from TDI should be clocked in while cs is low
	always @ (*) begin
		done_c = done;
		cycle_c = cycle;
		data_c = data;
		bytesRead_c = bytesRead;
		if(TCS) begin
			done_c = 0;
			cycle_c = 0;
		end // while cs high reset
		else begin
			cycle_c =  cycle + 1;
			data_c = {TDI, data[7:1]};
			if(cycle == 0) begin
				data_c = {TDI, data[7:1]};
				done_c = 1;
				transcation[bytesRead] = data_c;
				bytesRead_c = bytesRead + 1;
			end // counter overflows read complete
			else begin
				done_c = 0;
			end //done not ready
		end // cs low
 	end // non edge triggered
	
	always @ (posedge TCK or TCS) begin
		done <= #1 done_c;
		cycle <= #1 cycle_c;
		data <= #1 data_c;
		bytesRead <= #1 bytesRead_c;
	end // FF dec
endmodule // Serializer