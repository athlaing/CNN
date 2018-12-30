module VISIOinterface(
							////////////////////	Clock Input	 	////////////////////	 
							CLOCK_50,						//	50 MHz
							////////////////////	Push Button		////////////////////
							KEY,							//	Pushbutton[3:0]
							////////////////////	DPDT Switch		////////////////////
							SW,								//	Toggle Switch[17:0]
							////////////////////	7-SEG Dispaly	////////////////////
							HEX0,							//	Seven Segment Digit 0
							HEX1,							//	Seven Segment Digit 1
							HEX2,							//	Seven Segment Digit 2
							HEX3,							//	Seven Segment Digit 3
							HEX4,							//	Seven Segment Digit 4
							HEX5,							//	Seven Segment Digit 5
							HEX6,							//	Seven Segment Digit 6
							HEX7,							//	Seven Segment Digit 7
							////////////////////////	LED		////////////////////////
							LEDG,							//	LED Green[8:0]
							LEDR,							//	LED Red[17:0]
							////////////////////	SD_Card Interface	////////////////
							SD_DAT,							//	SD Card Data
							SD_DAT3,						//	SD Card Data 3
							SD_CMD,							//	SD Card Command Signal
							SD_CLK,							//	SD Card Clock
							////////////////////	USB JTAG link	////////////////////
							TDI,  							// CPLD -> FPGA (data in)
							TCK,  							// CPLD -> FPGA (clk)
							TCS,  							// CPLD -> FPGA (CS)
							TDO  							// FPGA -> CPLD (data out)
	);

////////////////////////	Clock Input	 	////////////////////////
input			CLOCK_50;				//	50 MHz
////////////////////////	Push Button		////////////////////////
input	[3:0]	KEY;					//	Pushbutton[3:0]
////////////////////////	DPDT Switch		////////////////////////
input	[17:0]	SW;						//	Toggle Switch[17:0]
////////////////////////	7-SEG Dispaly	////////////////////////
output	[6:0]	HEX0;					//	Seven Segment Digit 0
output	[6:0]	HEX1;					//	Seven Segment Digit 1
output	[6:0]	HEX2;					//	Seven Segment Digit 2
output	[6:0]	HEX3;					//	Seven Segment Digit 3
output	[6:0]	HEX4;					//	Seven Segment Digit 4
output	[6:0]	HEX5;					//	Seven Segment Digit 5
output	[6:0]	HEX6;					//	Seven Segment Digit 6
output	[6:0]	HEX7;					//	Seven Segment Digit 7
////////////////////////////	LED		////////////////////////////
output	[8:0]		LEDG;					//	LED Green[8:0]
output	[17:0]	LEDR;					//	LED Red[17:0]
////////////////////	SD Card Interface	////////////////////////
inout			SD_DAT;					//	SD Card Data
inout			SD_DAT3;				//	SD Card Data 3
inout			SD_CMD;					//	SD Card Command Signal
output		SD_CLK;					//	SD Card Clock

////////////////////	USB JTAG link	////////////////////////////
input  			TDI;					// CPLD -> FPGA (data in)
input  			TCK;					// CPLD -> FPGA (clk)
input  			TCS;					// CPLD -> FPGA (CS)
output 			TDO;					// FPGA -> CPLD (data out)

assign LEDR[17:8] = SW[17:8];

Receiver u0(	.TDI		(TDI),
					.TCS		(TCS),
					.TCK		(TCK),
					.data		(LEDR[7:0]),
					.done		(LEDG[1]));

Transmitter u1(	.TDO	(TDO),
						.TCS	(TCS),
						.TCK	(TCK),
						.data (SW[7:0]),
						.done	(LEDG[0]));

endmodule