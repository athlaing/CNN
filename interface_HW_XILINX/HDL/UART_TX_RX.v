module Uart_Rx
	(	
		Reset,
		inRx, 		
		CLK, 
		RxByte,
		Busy
	);
	
	parameter CLK_BIT   = 10'd87; // Default 10 MHz/115200 baudrate
	
	// states in rx line FSM
	// looks for start bit
	parameter IDLE 		= 2'b00;
	// waits half start bit
	parameter START     = 2'b01; 
	// Count clk cycles for each bit and record bit value
	parameter LOAD 		= 2'b10; 
	// Maintains complete state for at least 1 bit
	parameter COMPLETE  = 2'b11;
	
	input				Reset;			// Active-high reset for FSM
	input 				inRx;			// RX line from USB host
	input 				CLK;			// clk for 115200 baud rate
	output reg	[7:0]	RxByte = 8'h00;	// Displays the byte decoded after stop bit
	output reg			Busy = 1'b0; 	// Busy line used to determine currently reading
	
	// Holds the states for FSM
	reg 		[1:0]	state = IDLE;
	reg         [1:0]   state_c = IDLE;
	// counts the number of bits per transaction
	reg 		[2:0]	bitCount = 0;
	reg 		[2:0]	bitCount_c = 0;	
	// keep tracks of the current byte data 	
	reg 		[7:0]	RxByte_c = 0;				
	// reg used to count cycles for each bit supports ARTY-7 100Mhz/115200
	reg 		[9:0]   clkCount = 0;
	reg 		[9:0]   clkCount_c = 0;	
	// Rx line clked twice for metastability
	reg                 inRx_r = 1;
	reg                 Rx = 1;
		
	always @(*) begin
		Busy =  1'b0;
		state_c = state;
		RxByte_c = RxByte;
		bitCount_c = bitCount;
		clkCount_c = clkCount + 10'h001;
		case (state)
			IDLE: begin
				if(Rx == 1'b0)  begin
					Busy =  1'b1;
					state_c = START;
					clkCount_c = 10'h000;
				end // start bit found
			end // state while waiting for start bit
			START: begin
				Busy = 1'b1;
			    if(clkCount >= (CLK_BIT >> 2)) begin
					state_c = LOAD;
					clkCount_c = 10'h000;
					RxByte_c = 8'h00;
					bitCount_c = 3'b000;
					if(Rx != 1'b0) begin
						state_c = IDLE;
					end // go to idle  if not in start bit avoid spikes
			    end // go to load state after half start bit sample
			end // counted upto center sample
			LOAD: begin
				Busy = 1'b1;
				if(clkCount >= CLK_BIT) begin
				    clkCount_c = 10'h000;
					RxByte_c = {Rx, RxByte[7:1]};
                    bitCount_c = bitCount +  3'b001;
					if(bitCount == 3'b111) begin
						bitCount_c = 3'b000;
						state_c = COMPLETE;
					end  // complete overflow
				end // max sample per bit met
			end // state while loading
		    COMPLETE: begin
				Busy = 1'b1;
				if(clkCount >= CLK_BIT) begin
				    clkCount_c = 10'h000;
					state_c = IDLE;
				end // max sample per bit met
			end // state while loading
		endcase // FSM cases
		if(Reset == 1'b1) begin
			Busy = 1'b0;
		    state_c = IDLE;
            clkCount_c = 10'h000;
			RxByte_c =  8'h00;
			bitCount_c = 3'b000;
		end // reset conditions
	end // comb regs
	
	always @(posedge CLK) begin
		clkCount <= #1 clkCount_c;
		state <= #1 state_c;
		RxByte <= #1 RxByte_c;
		bitCount <= #1 bitCount_c;
		inRx_r <= #1 inRx;
		Rx <= #1 inRx_r;
	end // clked regs
endmodule // Uart_rx

module Uart_Tx
	(	
		Reset,
		Send,
		SendByte, 		// writing to  computer host
		CLK,  		// clk for 115200 baud rate
		Tx,
		Busy
	);
	
	// Default 10 MHz/115200 baudrate
	parameter CLK_BIT   = 10'd87;
	// states in rx line FSM
	// Wait for send condition
	parameter IDLE 		= 2'b00;
	// Set Tx line to current value of SendByte
	parameter SEND 		= 2'b10;
	// Maintains complete state for at least 1 bit
	parameter COMPLETE  = 2'b11;
	
	input				Reset;		 // Active-high reset for FSM
	input 				Send;		 // Trigger used to start sending byte
	input 		[7:0]	SendByte;    // Byte to be written to host USB
	input 				CLK;		 // CLK to count cycles
	output reg			Tx = 1'b1;   // Tx line from uart 
	output reg			Busy = 1'b0; // Busy line used to determine currently writing
	
	// holds the the sendbyte along with start and stop bits
	wire		[9:0] 	SendPacket;
	// Holds the states for FSM
	reg 		[1:0]	state = IDLE;
	reg         [1:0]   state_c = IDLE;
	// counts the number of bits per transaction
	reg 		[3:0]	bitCount = 0;
	reg 		[3:0]	bitCount_c = 0;	// counts the number of bits per transaction	
	// reg used to count cycles for each bit supports ARTY-7 100Mhz/115200
	reg 		[9:0]   clkCount = 0;
	reg 		[9:0]   clkCount_c = 0;	
	
	// add stop and start bits
	assign SendPacket = {{1'b1, SendByte}, 1'b0}; 
	
	always @(*) begin
		Busy =  1'b0;
		state_c = state;
		bitCount_c = bitCount;
		clkCount_c = clkCount + 10'h001;
		case (state)
			IDLE: begin
				if(Send == 1'b1)  begin
					Busy  = 1'b1;
					state_c = SEND;
					clkCount_c = 10'h000;
					bitCount_c = 4'h0;
				end // Start to send trigger detected
			end // wait until start trigger
			SEND: begin
				Busy = 1'b1;
				Tx = SendPacket[bitCount];
				if(clkCount >= CLK_BIT) begin
				    clkCount_c = 10'h000;
                    bitCount_c = bitCount +  4'h1;
					if(bitCount == 4'h9) begin
						bitCount_c = 4'h0;
						state_c = COMPLETE;
					end  // 10 Bits sent Start Bit / Byte / Stop bit
				end // Change Tx line to next bit in SendPacket
			end // Send individual bits of send Packet
			COMPLETE: begin
				Busy = 1'b1;
				Tx = 1'b1;
				if(clkCount >= CLK_BIT) begin	
					Busy = 1'b0;
				    clkCount_c = 10'h000;
					state_c = IDLE;
				end // 1 Bit passed
			end // Hold Tx line for at least 1 bit
		endcase // FSM cases
		if(Reset == 1'b1) begin
		    state_c = IDLE;
		    Tx = 1'b1;
			Busy = 1'b0;
            clkCount_c = 10'h000;
			bitCount_c = 4'h0;
		end // reset conditions
	end // comb regs
	
	always @(posedge CLK) begin
		clkCount <= #1 clkCount_c;
		state <= #1 state_c;
		bitCount <= #1 bitCount_c;
	end // clked regs
endmodule // Uart_Tx