`timescale 10ps/1ps
`celldefine

module adder42(a, b, c, d, cin, carry, sum, cout);

    input a;
    input b;
    input c;
    input d;
    input cin;
    output carry;
    output sum;
    output cout;
    wire temp;

    adder32 fa_0(.a(a), .b(b), .cin(c), .cout(cout), .sum(temp));
    adder32 fa_1(.a(temp), .b(d), .cin(cin), .cout(carry), .sum(sum));

endmodule
`endcelldefine
