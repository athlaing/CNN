# check both golden version exhaustively to make sure golden works
# version 1 made by Arthur Hlaing
# version 2 made by Ben Li
#TODO make sure the interface are the same

import addmult_v1 as v1
import addmult_v2 as v2
import itertools
import argparse
import random
import sys
from datetime import datetime
random.seed(datetime.now())

parser = argparse.ArgumentParser(description='Check golden versions to make sure they have the same behavior.')
parser.add_argument("-r","--range", help="number of test cases to run", default=None)
parser.add_argument("-q","--quiet", help="run test without printing on terminal", default="True")
parser.add_argument("-v","--version", help="run test with specific versions, either 1 or 2", default=0)
parser.add_argument("-m","--mix", help="randomize test case list before testing", default="True")
parser.add_argument("-s","--strict", help="end test when run into error", default="True")

args = vars(parser.parse_args())


error_v1  = 0
error_v2  = 0
error_comp= 0
version   = int(args["version"])
randomize = args["mix"] == "True"
quiet     = args["quiet"] == "True"
strict    = args["strict"] == "True"
counter_a = 0
counter_b = 0

if (args["range"] == None):
    range = -1
else:
    range = int(args["range"])

# generate all possible combination
a_list = list(itertools.product([0,1], repeat=16))
b_list = list(itertools.product([0,1], repeat=16))

if (range != -1):
    num_test = range ** 2
else:
    num_test = len(a_list) ** 2

if(randomize):
    random.shuffle(a_list)
    random.shuffle(b_list)
try:
    for a in a_list[:range]:
        a = ''.join([str(x) for x in a])
        counter_a += 1

        for b in b_list[:range]:
            b = ''.join([str(x) for x in b])
            counter_b += 1

            if(not quiet):
                print("a = "+a)
                print("b = "+b)

            #version 1
            if (version == 0 or version == 1):
                try:
                    a_v1 = v1.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
                    b_v1 = v1.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
                    c_v1 = v1.bfloat_mult(a_v1,b_v1).display_bin()

                    if(not quiet):
                        print("Version 1: ",c_v1)
                except Exception as e:
                    if (strict):
                        print(e)
                        sys.exit(1)
                    error_v1 += 1

            #version 2
            if (version == 0 or version == 2):
                try:
                    a_v2 = v2.bfloat(a)
                    b_v2 = v2.bfloat(b)
                    c_v2 = v2.mult_bfloat16(a_v2, b_v2).bin_parsed()

                    if(not quiet):
                        print("Version 2: ",c_v2)
                        print("="*15)
                except Exception as e:
                    if (strict):
                        print(e)
                        sys.exit(1)
                    error_v2 += 1

            #compare 2 versions:
            if (version == 0):
                pass #pass for now, both versions doesnt work

except KeyboardInterrupt:
    print("="*15)
    print("Percentage of pass test case version 1: " + str((counter_a*counter_b-error_v1)/(counter_a*counter_b)*100) + "% out of " + str(counter_a*counter_b) + " tests")
    print("Percentage of pass test case version 2: " + str((counter_a*counter_b-error_v2)/(counter_a*counter_b)*100) + "% out of " + str(counter_a*counter_b) + " tests")

if (version == 1):
    print("Percentage of pass test case version 1: " + str((num_test-error_v1)/num_test*100) + "% out of " + str(num_test) + " tests")
if (version == 2):
    print("Percentage of pass test case version 2: " + str((num_test-error_v2)/num_test*100) + "% out of " + str(num_test) + " tests")
