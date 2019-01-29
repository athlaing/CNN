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
parser.add_argument("-a","--adder", help="enable adder testbench generation.", default="True")
parser.add_argument("-m","--mult", help="enable mult testbench generation.", default="True")

args = vars(parser.parse_args())

randomize = args["mix"] == "True"
rg = int(args["range"]) 
stepsize = int(args["stepsize"])
add = args["adder"] == "True"
mult = args["mult"] == "True"
ts = '#' + str(2*stepsize)
cs = '#' + str(stepsize)

a_list = list(itertools.product([0,1], repeat=16))
b_list = list(itertools.product([0,1], repeat=16))

if(randomize):
    random.shuffle(a_list)
    random.shuffle(b_list)

if(mult)
    a_table = []
    b_table = []
    c_table = ['x'*16, 'x'*16]

    fvt_mult = open("mult_comb.vt", 'w')
    fref_mult = open("mult_ref.csv", 'w')
    fvt_mult.writelines(["module mult_comb_vt;\n",
        "\treg [15:0] a;\n",
        "\treg [15:0] b;\n",
        "\twire [15:0] out;\n",
        "\treg clk;\n",
        "\tbfloat16_mult test(.clk(clk), .a(a), .b(b), .out(out));\n",
        "\tinteger fout;\n\n"])
    fvt_mult.writelines(["\tinitial begin\n",
        "\t\tclk = 0;\n",
        "\t\tfout = $fopen(\"mult_out.csv\", \"w\");\n\n"
         ])

    for a in a_list[:rg]:
        a = ''.join([str(x) for x in a])

        for b in b_list[:rg]:
            b = ''.join([str(x) for x in b])
            fvt_mult.writelines([
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
        fref_mult.writelines([a_table[i], ',' , b_table[i], ',' , c_table[i], '\n'])

    fvt_mult.writelines([
        "\t\t", ts, ";\n",
        "\t\t", ts, ";\n",
        "\t\t$fclose(fout);\n"
        "\t\t$finish;\n\n"
    ])

    fvt_mult.write("\tend\n\n")
    fvt_mult.writelines([
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

    fvt_mult.close()
    fref_mult.close()
#end if(mult):

if(add):
    fvt_add = open("add_comb.vt", 'w')
    fref_add = open("add_ref.csv", 'w')
    fvt_add.writelines(["module add_comb_vt;\n",
        "\treg [15:0] a;\n",
        "\treg [15:0] b;\n",
        "\twire [15:0] out;\n",
        "\treg clk;\n",
        "\tbfloat16_adder test(.clk(clk), .a(a), .b(b), .out(out));\n",
        "\tinteger fout;\n\n"])
    fvt_add.writelines(["\tinitial begin\n",
        "\t\tclk = 0;\n",
        "\t\tfout = $fopen(\"add_out.csv\", \"w\");\n\n"
         ])
    
    for a in a_list[:rg]:
        a = ''.join([str(x) for x in a])

        for b in b_list[:rg]:
            b = ''.join([str(x) for x in b])
            fvt_add.writelines([
                "\t\ta = 16'b", a ,";\n",
                "\t\tb = 16'b", b ,";\n",
                "\t\t", ts, "\n\n"
            ])
            a_v2 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
            b_v2 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
            print(a_v2.display_bin(), b_v2.display_bin())
            print(a_v2.display_dec(), b_v2.display_dec())
            c_v2 = v2.bfloat_add(a_v2, b_v2)
            a_table.append(a)
            b_table.append(b)
            c_table.append(c_v2.bin())
    a_table.extend([a_table[-1], a_table[-1]])
    b_table.extend([b_table[-1], b_table[-1]])

    for i in range(len(a_table)):
        fref_add.writelines([a_table[i], ',' , b_table[i], ',' , c_table[i], '\n'])

    fvt_add.writelines([
        "\t\t", ts, ";\n",
        "\t\t", ts, ";\n",
        "\t\t$fclose(fout);\n"
        "\t\t$finish;\n\n"
    ])

    fvt_add.write("\tend\n\n")
    fvt_add.writelines([
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

    fvt_add.close()
    fref_add.close()
#end if(add)