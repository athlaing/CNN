# check both golden version exhaustively to make sure golden works
# version 1 made by Arthur Hlaing
# version 2 made by Ben Li
#TODO make sure the interface are the same

import addmult_v1 as v1
import addmult_v2 as v2
import itertools
import argparse
import random

parser = argparse.ArgumentParser(description='Check golden versions to make sure they have the same behavior.')
parser.add_argument("-r","--range", help="number of test cases to run", default=None)
parser.add_argument("-q","--quiet", help="run test without printing on terminal", default=True)
parser.add_argument("-v","--version", help="run test with specific versions, either 1 or 2", default=0)
parser.add_argument("-m","--mix", help="randomize test case list before testing", default=True)

args = vars(parser.parse_args())


num_errors = 0

range     = int(args["range"])
randomize = args["mix"] == True
version   = int(args["version"])
quiet     = args["quiet"] == True
counter_a = 0
counter_b = 0

# generate all possible combination
a_list = list(itertools.product([0,1], repeat=16))
b_list = list(itertools.product([0,1], repeat=16))

if(randomize):
    random.shuffle(a_list)
    random.shuffle(b_list)

for a in a_list:
    for b in b_list:

        a = ''.join([str(x) for x in a])
        b = ''.join([str(x) for x in b])

        if(not quiet):
            print("a = "+a)
            print("b = "+b)

        #version 1
        if (version == 0 or version == 1):
            a_v1 = v1.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
            b_v1 = v1.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
            c_v1 = v1.bfloat_mult(a_v1,b_v1)

            if(not quiet):
                print("Version 1: ",c_v1)

        #version 2
        if (version == 0 or version == 2):
            a_v2 = v2.bfloat(a)
            b_v2 = v2.bfloat(b)
            c_v2 = v2.mult_bfloat16(a_v2, b_v2).bin_parsed()

            if(not quiet):
                print("Version 2: ",c_v2)
                print("="*15)

        #compare 2 versions:
        if (version == 0):
            pass #pass for now, both versions doesnt work

        #counter
        if (range != None and counter_b < range):
            counter_b += 1
        elif (range != None and counter_b == range):
            break

    #counter
    if (range != None and counter_a < range):
        counter_a += 1
    elif (range != None and counter_a == range):
        break
