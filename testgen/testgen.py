#Testbench generator for mult and adder
#
#TODO: Adder gen

import itertools
import random
import argparse

parser = argparse.ArgumentParser(description='Generate testbench files for mult_comb.v and add_comb.v')
parser.add_argument("-r","--range", help="number of test cases to run", default=2)
parser.add_argument("-m","--mix", help="randomize test case list before testing", default="True")
parser.add_argument("-s","--stepsize", help="stepsize for the simulation in picoseconds", default=10)
args = vars(parser.parse_args())

randomize = args["mix"] == "True"
range = int(args["range"]) 
stepsize = int(args["stepsize"])
ts = '#' + str(2*stepsize)
cs = '#' + str(stepsize)

a_list = list(itertools.product([0,1], repeat=16))
b_list = list(itertools.product([0,1], repeat=16))

if(randomize):
    random.shuffle(a_list)
    random.shuffle(b_list)

f = open("mult_comb.vt", 'w')
f.writelines(["module mult_comb_vt;\n",
    "\treg [15:0] a;\n",
    "\treg [15:0] b;\n",
    "\twire [15:0] out;\n",
    "\treg clk;\n",
    "\tbfloat16_mult test(.clk(clk), .a(a), .b(b), .out(out));\n",
    "\tinteger fout;\n\n"])
f.writelines(["\tinitial begin\n",
    "\t\tclk = 0;\n",
    "\t\tfout = $fopen(\"mult_out.csv\", \"w\");\n\n"
     ])


for a in a_list[:range]:
    a = ''.join([str(x) for x in a])

    for b in b_list[:range]:
        b = ''.join([str(x) for x in b])
        f.writelines([
            "\t\ta = 16'b", a ,";\n",
            "\t\tb = 16'b", b ,";\n",
            "\t\t", ts, "\n\n"
        ])

f.writelines([
    "\t\t", ts, ";\n",
    "\t\t", ts, ";\n",
    "\t\t$fclose(fout);\n"
    "\t\t$finish;\n\n"
])

f.write("\tend\n\n")
f.writelines([
    "\talways begin\n",
    "\t\tclk = ~clk;\n",
    "\t\t", cs, ";\n",
    "\tend\n\n",
    "\talways begin\n",
    "\t\t$fwrite(fout, \"%b,%b,%b\\n\", a, b, out);\n",
    "\t\t", ts, ";\n"
    "\tend\n",
    "endmodule"
    ])
f.close()