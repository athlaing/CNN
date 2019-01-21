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
import tqdm
import time
from datetime import datetime
random.seed(datetime.now())

parser = argparse.ArgumentParser(description='Check golden versions to make sure they have the same behavior.')
parser.add_argument("-r","--range", help="number of test cases to run", default=None)
parser.add_argument("-q","--quiet", help="run test without printing on terminal", default="True")
parser.add_argument("-v","--version", help="run test with specific versions, either 1 or 2", default=0)
parser.add_argument("-m","--mix", help="randomize test case list before testing", default="True")
parser.add_argument("-s","--strict", help="end test when run into error", default="True")
parser.add_argument("-t","--threetwo", help="compare with 32 bit version", default="True")
parser.add_argument("-e","--epsilon", help="accuracy threshold with 32 bit", default=0.1)
parser.add_argument("-p","--product", help="test multiplier", default="True")
parser.add_argument("-a","--addition", help="test adder", default="True")
parser.add_argument("-d","--detailed", help="Display more detail; use with --quiet.", default= "False")

args = vars(parser.parse_args())

error_acc_v1 = 0
error_acc_v2 = 0
error_v1  = 0
error_v2  = 0
error_s   = 0
error_e   = 0
error_m   = 0
counter   = 0
version   = int(args["version"])
epsilon   = float(args["epsilon"])
randomize = args["mix"] == "True"
mult      = args["product"] == "True"
add       = args["addition"] == "True"
quiet     = args["quiet"] == "True"
strict    = args["strict"] == "True"
compare_32= args["threetwo"] == "True"
detail    = args["detailed"] == "True"
interrupt = False

if (args["range"] == None):
    range = -1
else:
    range = int(args["range"])

# generate all possible combination
a_list = list(itertools.product([0,1], repeat=16))
b_list = list(itertools.product([0,1], repeat=16))

bfloat_min = v2.bfloat('0', '00000000' , '0000001').display_dec()
bfloat_max = v2.bfloat('0', '11111110' , '1111111').display_dec()

if (range != -1):
    num_test = range ** 2
else:
    num_test = len(a_list) ** 2

if(randomize):
    random.shuffle(a_list)
    random.shuffle(b_list)
    
#Test Multiplier    
if(mult):
    print ("************* Multiplier performance *************")
    print ("Progress bar:")
    try:
        for a in tqdm.tqdm(a_list[:range]):
            a = ''.join([str(x) for x in a])
    
            for b in b_list[:range]:
                b = ''.join([str(x) for x in b])
                counter += 1
    
                if(not quiet):
                    print("a = "+a)
                    print("b = "+b)
                    
                #version 1
                if (version == 0 or version == 1):
                    try:
                        a_v1 = v1.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
                        b_v1 = v1.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
                        raw_v1 = v1.bfloat_mult(a_v1,b_v1)
                        c_v1   = raw_v1.display_bin()
                        c_16_v1 = raw_v1.display_dec()
                        
                        if(not quiet):
                            print("Version 1: ",c_v1)
                            if(detail):
                                print("V1 a dec:", a_v2.display_dec())
                                print("V1 b dec:", b_v2.display_dec())
                                print("V1 c dec:", c_16_v2)
                                print("V1 c bin:", c_v2)
                        
                        #compare 32-bit version
                        if (compare_32):
                            a_32 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:])).display_dec()
                            b_32 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:])).display_dec()
                            c_32 = a_32 * b_32
                            
                            if abs(c_32) == 0.0 or abs(c_16_v2) == 0.0:
                                diff_v2 = 0.0
                            elif abs(c_32) == float("Inf") or abs(c_16_v2) == float("Inf"):
                                diff_v2 = 0.0
                            else:
                                diff_v2 = abs((c_32-c_16_v2)/(c_32))

                            if (diff_v2 >= epsilon):
                                if (strict):
                                    assert False, "error larger than epsilon"
                                error_acc_v2 += 1
                                if (not quiet):
                                    print("Version 2 accuracy with 32 bit is " + str(diff_v2) + 
                                          " 16-bit: " + str(c_16_v2) +
                                          " 32-bit: " + str(c_32))                                
                    except Exception as e:
                        if (strict):
                            print(e)
                            sys.exit(1)
                        error_v1 += 1
    
                #version 2
                if (version == 0 or version == 2):
                    try:
                        a_v2 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
                        b_v2 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
                        raw_v2 = v2.bfloat_mult(a_v2,b_v2)
                        c_v2   = raw_v2.display_bin()
                        c_16_v2 = raw_v2.display_dec()
                                            
                        if(not quiet):
                            print("Version 2: ", c_v2)
                            if(detail):
                                print("v2 a dec:", a_v2.display_dec())
                                print("v2 b dec:", b_v2.display_dec())
                                print("v2 c dec:", c_16_v2)
                                print("v2 c bin:", c_v2)
                            
                            
                        #compare 32-bit version
                        if (compare_32):
                            a_32 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:])).display_dec()
                            b_32 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:])).display_dec()
                            c_32 = a_32 * b_32
                            if abs(c_32) == 0.0 or abs(c_16_v2) == 0.0:
                                diff_v2 = 0.0
                            elif abs(c_32) == float("Inf") or abs(c_16_v2) == float("Inf"):
                                diff_v2 = 0.0
                            else:
                                diff_v2 = abs((c_32-c_16_v2)/(c_32))
                            if (diff_v2 >= epsilon):
                                if (not quiet):
                                    print("Version 2 accuracy with 32 bit is " + str(diff_v2) + 
                                          " 16-bit: " + str(c_16_v2) +
                                          " 32-bit: " + str(c_32))
                                if (strict):
                                    assert False, "error larger than epsilon"
                                error_acc_v2 += 1
                        
                        if(not quiet):   
                            print("="*15)    
                                  
                    except Exception as e:
                        if (strict):
                            print(e)
                            sys.exit(1)
                        error_v2 += 1
    
                #compare 2 versions:
                if (version == 0):
                    sign_pred = c_v1[0] == c_v2[0]
                    exp_pred  = c_v1[1] == c_v2[1]
                    man_pred  = c_v1[2] == c_v2[2]
                    pred = sign_pred and exp_pred and man_pred
                    
                    if (strict and not pred):
                        assert sign_pred, "Sign bit is different"
                        assert exp_pred, "Exp bits are different"
                        assert man_pred, "Man bits are different"
                        
                    if (not sign_pred):
                        error_s += 1
                        if(not quiet):
                            print ("Wrong sign: v1: " + str(c_v1[0]) + " v2 "+ str(c_v2[0]))
                    if (not exp_pred):
                        error_e += 1
                        if(not quiet):
                            print ("Wrong exp: v1: " + str(c_v1[1]) + " v2 "+ str(c_v2[1]))
                    if (not man_pred):
                        error_m += 1
                        if(not quiet):
                            print ("Wrong sign: v1: " + str(c_v1[2]) + " v2 "+ str(c_v2[2]))
                            
    
    except KeyboardInterrupt:
        interrupt = True
        print(" ")
        print("="*50)
        if (version == 1 or version == 0):
            
            print("Percentage of runable test case version 1: " + str((counter-error_v1)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 1: " + str((counter-error_acc_v1)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 2 or version == 0):
            
            print("Percentage of runable test case version 2: " + str((counter-error_v2)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 2: " + str((counter-error_acc_v2)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 0): 
            
            print("Percentage of agreed (1 vs 2) test case correct s: " + str((counter-error_s)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct e: " + str((counter-error_e)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct m: " + str((counter-error_m)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
        print("="*50)
    
    if(not interrupt):
        print("="*50)
        if (version == 1 or version == 0):
            
            print("Percentage of runable test case version 1: " + str((num_test-error_v1)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 1: " + str((num_test-error_acc_v1)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 2 or version == 0):
            
            print("Percentage of runable test case version 2: " + str((num_test-error_v2)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 2: " + str((num_test-error_acc_v2)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 0): 
            
            print("Percentage of agreed (1 vs 2) test case correct s: " + str((num_test-error_s)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct e: " + str((num_test-error_e)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct m: " + str((num_test-error_m)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
        print("="*50)  

if(add):
    print ("************* Adder performance *************")
    print ("Progress bar:")
    try:
        for a in tqdm.tqdm(a_list[:range]):
            a = ''.join([str(x) for x in a])
    
            for b in b_list[:range]:
                b = ''.join([str(x) for x in b])
                counter += 1
    
                if(not quiet):
                    print("a = "+a)
                    print("b = "+b)
                    
                #version 1
                if (version == 0 or version == 1):
                    try:
                        a_v1 = v1.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
                        b_v1 = v1.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
                        raw_v1 = v1.bfloat_add(a_v1,b_v1)
                        c_v1   = raw_v1.display_bin()
                        c_16_v1 = raw_v1.display_dec()
                        
                        if(not quiet):
                            print("Version 1: ",c_v1)
                            if(detail):
                                print("V1 a dec:", a_v1.display_dec())
                                print("V1 b dec:", b_v1.display_dec())
                                print("V1 c dec:", c_16_v1)
                                print("V1 c bin:", c_v1)
                        
                        #compare 32-bit version
                        if (compare_32):
                            a_32 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:])).display_dec()
                            b_32 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:])).display_dec()
                            c_32 = a_32 + b_32
                            
                            if abs(c_32) == 0.0 or abs(c_16_v2) == 0.0:
                                diff_v2 = 0.0
                            elif abs(c_32) == float("Inf") or abs(c_16_v2) == float("Inf"):
                                diff_v2 = 0.0
                            else:
                                diff_v2 = abs((c_32-c_16_v2)/(c_32))

                            if (diff_v2 >= epsilon):
                                if (strict):
                                    assert False, "error larger than epsilon"
                                error_acc_v2 += 1
                                if (not quiet):
                                    print("Version 2 accuracy with 32 bit is " + str(diff_v2) + 
                                          " 16-bit: " + str(c_16_v2) +
                                          " 32-bit: " + str(c_32))                                
                    except Exception as e:
                        if (strict):
                            print(e)
                            sys.exit(1)
                        error_v1 += 1
    
                #version 2
                if (version == 0 or version == 2):
                    try:
                        a_v2 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:]))
                        b_v2 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:]))
                        raw_v2 = v2.bfloat_add(a_v2,b_v2)
                        c_v2   = raw_v2.display_bin()
                        c_16_v2 = raw_v2.display_dec()
                                            
                        if(not quiet):
                            print("Version 2: ", c_v2)
                            if(detail):
                                print("v2 a dec:", a_v2.display_dec())
                                print("v2 b dec:", b_v2.display_dec())
                                print("v2 c dec:", c_16_v2)
                                print("v2 c bin:", c_v2)
                            
                            
                        #compare 32-bit version
                        if (compare_32):
                            a_32 = v2.bfloat(str(a[0]),str(a[1:9]),str(a[9:])).display_dec()
                            b_32 = v2.bfloat(str(b[0]),str(b[1:9]),str(b[9:])).display_dec()
                            c_32 = a_32 + b_32
                            if not quiet:
                                print("v2 float32:", c_32)
                            if abs(c_32) == 0.0 or abs(c_16_v2) == 0.0:
                                diff_v2 = 0.0
                            elif abs(c_32) == float("Inf") or abs(c_16_v2) == float("Inf"):
                                diff_v2 = 0.0
                            else:
                                diff_v2 = abs((c_32-c_16_v2)/(c_32))

                                if (diff_v2 >= epsilon):        
                                    print("Version 2 accuracy with 32 bit is " + str(diff_v2) + 
                                          " 16-bit: " + str(c_16_v2) +
                                          " 32-bit: " + str(c_32))                                
                                    if (strict):
                                        assert False, "error larger than epsilon"
                                    error_acc_v2 += 1

                            if(not quiet):
                                print("="*15)
                                    
                    except Exception as e:
                        if (strict):
                            print(e)
                            sys.exit(1)
                        error_v2 += 1
    
                #compare 2 versions:
                if (version == 0):
                    sign_pred = c_v1[0] == c_v2[0]
                    exp_pred  = c_v1[1] == c_v2[1]
                    man_pred  = c_v1[2] == c_v2[2]
                    pred = sign_pred and exp_pred and man_pred
                    
                    if (strict and not pred):
                        assert sign_pred, "Sign bit is different"
                        assert exp_pred, "Exp bits are different"
                        assert man_pred, "Man bits are different"
                        
                    if (not sign_pred):
                        error_s += 1
                        if(not quiet):
                            print ("Wrong sign: v1: " + str(c_v1[0]) + " v2 "+ str(c_v2[0]))
                    if (not exp_pred):
                        error_e += 1
                        if(not quiet):
                            print ("Wrong exp: v1: " + str(c_v1[1]) + " v2 "+ str(c_v2[1]))
                    if (not man_pred):
                        error_m += 1
                        if(not quiet):
                            print ("Wrong sign: v1: " + str(c_v1[2]) + " v2 "+ str(c_v2[2]))
                            
    
    except KeyboardInterrupt:
        interrupt = True
        print(" ")
        print("="*50)
        if (version == 1 or version == 0):
            
            print("Percentage of runable test case version 1: " + str((counter-error_v1)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 1: " + str((counter-error_acc_v1)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 2 or version == 0):
            
            print("Percentage of runable test case version 2: " + str((counter-error_v2)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 2: " + str((counter-error_acc_v2)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 0): 
            
            print("Percentage of agreed (1 vs 2) test case correct s: " + str((counter-error_s)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct e: " + str((counter-error_e)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct m: " + str((counter-error_m)/(counter)*100) + 
                  "% out of " + str(counter) + " tests")
            
        print("="*50)
    
    if(not interrupt):
        print("="*50)
        if (version == 1 or version == 0):
            
            print("Percentage of runable test case version 1: " + str((num_test-error_v1)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 1: " + str((num_test-error_acc_v1)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 2 or version == 0):
            
            print("Percentage of runable test case version 2: " + str((num_test-error_v2)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            if (compare_32):
                print("Percentage of pass 32-bit comparison version 2: " + str((num_test-error_acc_v2)/(counter)*100) + 
                      "% out of " + str(counter) + " tests")
            
        if (version == 0): 
            
            print("Percentage of agreed (1 vs 2) test case correct s: " + str((num_test-error_s)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct e: " + str((num_test-error_e)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
            print("Percentage of agreed (1 vs 2) test case correct m: " + str((num_test-error_m)/num_test*100) + 
                  "% out of " + str(num_test) + " tests")
            
        print("="*50)            