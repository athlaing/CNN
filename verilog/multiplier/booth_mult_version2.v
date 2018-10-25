module boothMult(input_a, input_b, clk, ready, result_r);

  //IO and connection
  input  wire [8:0] input_a;
  input  wire [8:0] input_b;
  input  wire clk;
  output reg  ready;
  output reg [11:0] result_r;
  reg state, state_c;
  wire   [11:0] row_0_ca, row_1_ca;
  wire   cout_0, cout_1, cout_2, cout_3, cout_4, cout_5, cout_6, cout_7, cout_8, cout_9, cout_10, cout_11;

  //cases
  parameter EXTEND = 2'b00;
  parameter MOVE   = 2'b01;
  parameter ADD    = 2'b10;
  parameter READY  = 2'b11;

  //EXTEND related
  reg [11:0] row_0_x, row_1_x, row_2_x, row_3_x;

  //MOVE related
  reg [11:0] row_0_x_r, row_1_x_r, row_2_x_r, row_3_x_r;

  //ADD related
  reg [11:0] row_0_ca_r, row_1_ca_r;

  //READY related
  reg result;

  //look-up table instantiation
  wire   [8:0]  row_0, row_1, row_2, row_3;
  boothEncoding e_module_0(.a(input_a),.encoding(input_b[2:0]),.pp(row_0));
  boothEncoding e_module_1(.a(input_a),.encoding(input_b[4:2]),.pp(row_1));
  boothEncoding e_module_2(.a(input_a),.encoding(input_b[6:4]),.pp(row_2));
  boothEncoding e_module_3(.a(input_a),.encoding(input_b[8:6]),.pp(row_3));

  //adder42 instantiation
  wire  [11:0] connection_0, connection_1, connection_2, connection_3;
  adder42 a42_module_0(.a(connection_0[3]), .b(connection_1[3]), .c(connection_2[3]), .d(connection_3[3]),
                     .cin(cout_2), .carry(row_1_ca[3]), .sum(row_0_ca[3]), .cout(cout_3));
  adder42 a42_module_1(.a(connection_0[4]), .b(connection_1[4]), .c(connection_2[4]), .d(connection_3[4]),
                     .cin(cout_3), .carry(row_1_ca[4]), .sum(row_0_ca[4]), .cout(cout_4));
  adder42 a42_module_2(.a(connection_0[5]), .b(connection_1[5]), .c(connection_2[5]), .d(connection_3[5]),
                     .cin(cout_4), .carry(row_1_ca[5]), .sum(row_0_ca[5]), .cout(cout_5));
  adder42 a42_module_3(.a(connection_0[6]), .b(connection_1[6]), .c(connection_2[6]), .d(connection_3[6]),
                     .cin(cout_5), .carry(row_1_ca[6]), .sum(row_0_ca[6]), .cout(cout_6));
  adder42 a42_module_4(.a(connection_0[7]), .b(connection_1[7]), .c(connection_2[7]), .d(connection_3[7]),
                     .cin(cout_6), .carry(row_1_ca[7]), .sum(row_0_ca[7]), .cout(cout_7));
  adder42 a42_module_5(.a(connection_0[8]), .b(connection_1[8]), .c(connection_2[8]), .d(connection_3[8]),
                     .cin(cout_7), .carry(row_1_ca[8]), .sum(row_0_ca[8]), .cout(cout_8));
  adder42 a42_module_6(.a(connection_0[9]), .b(connection_1[9]), .c(connection_2[9]), .d(connection_3[9]),
                     .cin(cout_8), .carry(row_1_ca[9]), .sum(row_0_ca[9]), .cout(cout_9));
  adder42 a42_module_7(.a(connection_0[10]),.b(connection_1[10]),.c(connection_2[10]),.d(connection_3[10]),
                     .cin(cout_9), .carry(row_1_ca[10]),.sum(row_0_ca[10]),.cout(cout_10));
  adder42 a42_module_8(.a(connection_0[11]),.b(connection_1[11]),.c(connection_2[11]),.d(connection_3[11]),
                     .cin(cout_10), .carry(row_1_ca[11]),.sum(row_0_ca[11]),.cout(cout_11));

  //adder32 instantiation
  adder32 a32_module(.a(connection_0[2]), .b(connection_1[2]), .c(connection_2[2]),
                     .cout(row_1_ca[2]), .sum(row_0_ca[2]));

   always @(*) begin
      case(state)
         /*===================================================================*/
         EXTEND: begin
             row_0_x = { {3{row_0[8]}},row_0};
             row_1_x = {{{2{row_1[8]}},row_0},1'b0};
             row_2_x = {{{row_2[8],row_0}},2'b00};
             row_3_x = {row_3,3'b000};
             state_c = MOVE;
         end
         /*===================================================================*/
         MOVE: begin
             //FA and firt position
             connection_0 = row_0_x_r;
             connection_1 = row_1_x_r;
             connection_2 = row_2_x_r;
             connection_3 = row_3_x_r;
             {row_0_ca_r[1], row_1_ca_r[1]} = row_0_x_r[1] + row_1_x_r[1];
             row_0_ca_r[0] = 0;
             row_1_ca_r[0] = row_0_x_r[0];
             state_c = ADD;
         end
         /*===================================================================*/
         ADD: begin
             result  = row_0_ca_r + row_1_ca_r;
             ready   = 1;
             state_c = READY;
         end
         /*===================================================================*/
         READY: begin
             state_c = EXTEND;
             ready   = 0;
         end
      endcase
   end
   always @(posedge clk) begin
     state        <= state_c;
     row_0_x_r <= row_0_x;
     row_1_x_r <= row_1_x;
     row_2_x_r <= row_2_x;
     row_3_x_r <= row_3_x;
     result_r     <=  result;
     row_0_ca_r[11:2] <= row_0_ca[11:2];
     row_1_ca_r[11:2] <= row_1_ca[11:2];
   end
endmodule
