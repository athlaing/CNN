#Testbench generator for mult and adder
#
#TODO: testgen for adder
#      option for which golden version to use

import sys
sys.path.append('../golden/basic_logic')
import itertools
import random
import argparse
import addmult_v2 as v2

parser = argparse.ArgumentParser(description='Generate testbench files for mult_comb.v and add_comb.v')
parser.add_argument("-r","--range", help="number of test cases to run", default=2)
parser.add_argument("-m","--mix", help="randomize test case list before testing", default="True")
parser.add_argument("-s","--stepsize", help="stepsize for the simulation in picoseconds", default=10)
args = vars(parser.parse_args())

randomize = args["mix"] == "True"
rg = int(args["range"]) 
stepsize = int(args["stepsize"])
ts = '#' + str(2*stepsize)
cs = '#' + str(stepsize)

a_list = list(itertools.product([0,1], repeat=16))
b_list = list(itertools.product([0,1], repeat=16))
a_table = []
b_table = []
c_table = ['x'*16, 'x'*16]

if(randomize):
    random.shuffle(a_list)
    random.shuffle(b_list)

fvt = open("mult_comb.vt", 'w')
fref = open("mult_ref.csv", 'w')
fvt.writelines(["module mult_comb_vt;\n",
    "\treg [15:0] a;\n",
    "\treg [15:0] b;\n",
    "\twire [15:0] out;\n",
    "\treg clk;\n",
    "\tbfloat16_mult test(.clk(clk), .a(a), .b(b), .out(out));\n",
    "\tinteger fout;\n\n"])
fvt.writelines(["\tinitial begin\n",
    "\t\tclk = 0;\n",
    "\t\tfout = $fopen(\"mult_out.csv\", \"w\");\n\n"
     ])

for a in a_list[:rg]:
    a = ''.join([str(x) for x in a])

    for b in b_list[:rg]:
        b = ''.join([str(x) for x in b])
        fvt.writelines([
            "\t\ta = 16'b", a ,";\n",
            "\t\tb = 16'b", b ,";\n",
            "\t\t", ts, "\n\n"
        ])
        a_v2 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
        b_v2 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
        c_v2 = v2.bfloat_mult(a_v2, b_v2)
        a_table.append(a)
        b_table.append(b)
        c_table.append(c_v2.bin())
a_table.extend([a_table[-1], a_table[-1]])
b_table.extend([b_table[-1], b_table[-1]])

for i in range(len(a_table)):
    fref.writelines([a_table[i], ',' , b_table[i], ',' , c_table[i], '\n'])

fvt.writelines([
    "\t\t", ts, ";\n",
    "\t\t", ts, ";\n",
    "\t\t$fclose(fout);\n"
    "\t\t$finish;\n\n"
])

fvt.write("\tend\n\n")
fvt.writelines([
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

fvt.close()
fref.close()