import numpy as np
import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu
format = alu.bfloat


def functional(input):
    input_d = len(input)

    #TODO======================
    #   SUPER IMPORTANT:
    # This is tempo fix because there is no bfloat divide and exp
    # in future softmax should be able to support bfloat
    # input = list(map())
    #end TODO==================

    output =  [format('0')*16 for i in range*input_d]
    sum = format('0'*16)
    for i in range (input_s):
        sum += np.exp(input[i])
    for i in range (input_s):
        output_array[i] = np.exp(input[i])/sum
    return output_array
