module VISIOinterface(
    input CLK100MHZ,
    input  [3:0] btn,
    input  [3:0] sw,
    output [3:0] led,
    output uart_rxd_out,
    input uart_txd_in
    );
    wire [7:0] byte;
    
    //assign uart_rxd_out = uart_txd_in;
    //assign led[3] = btn[0];
    assign led[3:0] = (sw[0]) ? byte[7:4] : byte[3:0]; 
    
    Uart_Rx    #(   .CLK_BIT            (10'd868))
              u1(   .Reset              (btn[0]),
                    .inRx 		        (uart_txd_in), 
                    .CLK                (CLK100MHZ),
                    .RxByte             (byte),
                    .Busy               ());
                    
    Uart_Tx    #(   .CLK_BIT            (10'd868))
              u2(   .Reset              (btn[0]),	
                    .Send               (btn[2]),
                    .SendByte           (8'b0110_0001), 		
                    .CLK                (CLK100MHZ),  		
                    .Tx                 (uart_rxd_out),
                    .Busy               ());
    
endmodule