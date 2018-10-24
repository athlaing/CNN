module bfloat16_mult(reset, clk, a, b, out, ready);
    input reset, clk;
    input [15:0] a, b;
    output reg [15:0] out;
    output reg ready;

    //intermediate values
    reg [6:0] input_a;
    reg [8:0] input_b;
    reg [2:0] state, state_c;

    always @(*) begin
        case(state)
            /*===================================================================*/
            INIT: begin
                input_a = a;
                input_b = {b[6],{b,1'b0}};
                state_c = SHIFT;
            end

        endcase
    end

    always @(posedge clk) begin
        state   <= state_c;
        row_0_r <= row_0;
        row_1_r <= row_1;
        row_2_r <= row_2;
        row_3_r <= row_3;
        row_0_x_r <= row_0_x;
        row_1_x_r <= row_1_x;
        row_2_x_r <= row_2_x;
        row_3_x_r <= row_3_x;
    end
endmodule
