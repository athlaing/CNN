module boothMult(input_a, input_b, clk, ready);

  //IO and connection
  input  wire input_a, input_b, clk;
  output reg ready;
  output reg [11:0] result_r;
  wire   [8:0]  row_0, row_1, row_2, row_3;
  wire   [11:0] row_0_ca, row_1_ca;
  wire   cout_0, cout_1, cout_2, cout_3, cout_4, cout_5, cout_6, cout_7, cout_8, cout_9, cout_10, cout_11;
  wire   [11:0] row_0_x_r, row_1_x_r, row_2_x_r, row_3_x_r;

  //cases
  parameter SHIFT = 2'b00;
  parameter ADD   = 2'b01;
  parameter READY = 2'b10;

  //SHIFT related
  reg state, state_c;
  reg [11:0] row_0_x, row_1_x, row_2_x, row_3_x;

  //ADD related
  reg   [11:0] row_0_ca_r, row_1_ca_r;

  //READY related
  reg result;

  //look-up table instantiation
  boothEncoding e_module_0(.a(input_a),.encoding(input_b[2:0]),.pp(row_0));
  boothEncoding e_module_1(.a(input_a),.encoding(input_b[4:2]),.pp(row_1));
  boothEncoding e_module_2(.a(input_a),.encoding(input_b[6:4]),.pp(row_2));
  boothEncoding e_module_3(.a(input_a),.encoding(input_b[8:6]),.pp(row_3));

  //adder42 instantiation
  adder42 a42_module_0(.a(row_0_x_r[3]), .b(row_1_x_r[3]), .c(row_2_x_r[3]), .d(row_3_x_r[3]),
                     .cin(cout_2), .carry(row_1_ca[3]), .sum(row_0_ca[3]), .cout(cout_3));
  adder42 a42_module_1(.a(row_0_x_r[4]), .b(row_1_x_r[4]), .c(row_2_x_r[4]), .d(row_3_x_r[4]),
                     .cin(cout_3), .carry(row_1_ca[4]), .sum(row_0_ca[4]), .cout(cout_4));
  adder42 a42_module_2(.a(row_0_x_r[5]), .b(row_1_x_r[5]), .c(row_2_x_r[5]), .d(row_3_x_r[5]),
                     .cin(cout_4), .carry(row_1_ca[5]), .sum(row_0_ca[5]), .cout(cout_5));
  adder42 a42_module_3(.a(row_0_x_r[6]), .b(row_1_x_r[6]), .c(row_2_x_r[6]), .d(row_3_x_r[6]),
                     .cin(cout_5), .carry(row_1_ca[6]), .sum(row_0_ca[6]), .cout(cout_6));
  adder42 a42_module_4(.a(row_0_x_r[7]), .b(row_1_x_r[7]), .c(row_2_x_r[7]), .d(row_3_x_r[7]),
                     .cin(cout_6), .carry(row_1_ca[7]), .sum(row_0_ca[7]), .cout(cout_7));
  adder42 a42_module_5(.a(row_0_x_r[8]), .b(row_1_x_r[8]), .c(row_2_x_r[8]), .d(row_3_x_r[8]),
                     .cin(cout_7), .carry(row_1_ca[8]), .sum(row_0_ca[8]), .cout(cout_8));
  adder42 a42_module_6(.a(row_0_x_r[9]), .b(row_1_x_r[9]), .c(row_2_x_r[9]), .d(row_3_x_r[9]),
                     .cin(cout_8), .carry(row_1_ca[9]), .sum(row_0_ca[9]), .cout(cout_9));
  adder42 a42_module_7(.a(row_0_x_r[10]),.b(row_1_x_r[10]),.c(row_2_x_r[10]),.d(row_3_x_r[10]),
                     .cin(cout_9), .carry(row_1_ca[10]),.sum(row_0_ca[10]),.cout(cout_10));
  adder42 a42_module_8(.a(row_0_x_r[11]),.b(row_1_x_r[11]),.c(row_2_x_r[11]),.d(row_3_x_r[11]),
                     .cin(cout_10), .carry(row_1_ca[11]),.sum(row_0_ca[11]),.cout(cout_11));

  //adder32 instantiation
  adder32 a32_module(.a(row_0_x_r[2]), .b(row_1_x_r[2]), .c(row_2_x_r[2]),
                     .cout(row_1_ca[2]), .sum(row_0_ca[2]))

  //FA and firt position
  row_0_ca[1] = (row_0_x_r[1] + row_0_x_r[1])[0];
  row_1_ca[1] = (row_0_x_r[1] + row_0_x_r[1])[1];
  row_0_ca[0] = 0;
  row_1_ca[0] = row_0_x_r[0];

   always @(*) begin
      case(state)
         /*===================================================================*/
         SHIFT: begin
             row_0_x = { 3{row_0[8]},row_0};
             row_1_x = {{2{row_1[8]},row_0},1'b0};
             row_2_x = {{1{row_2[8]},row_0},2'b00};
             row_3_x = {row_3,2'b000};
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
             state_c = SHIFT;
             ready   = 0;
         end

   always @(posedge clk) begin
     state   <= state_c
     row_0_x_r <= row_0_x;
     row_1_x_r <= row_1_x;
     row_2_x_r <= row_2_x;
     row_3_x_r <= row_3_x;
     row_0_ca_r<= row_0_ca;
     row_1_ca_r<= row_1_ca;
     result_r  <=  result;
   end
endmodule
