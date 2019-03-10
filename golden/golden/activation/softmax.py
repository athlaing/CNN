import numpy as np
import math
import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu
format = alu.bfloat
bfloat2f = alu.bfloat2f


def functional(input):
    input_d = len(input)

    #TODO======================
    #   SUPER IMPORTANT:
    # This is tempo fix because there is no bfloat divide and exp
    # in future softmax should be able to support bfloat
    #end TODO==================

    input = list(map(bfloat2f,input))
    output =  []
    sum = 0
    for i in range (input_d):
        sum += math.exp(input[i])
    for i in range (input_d):
        output.append(math.exp(input[i])/sum)
    return output
