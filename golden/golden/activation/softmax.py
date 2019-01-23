import numpy as np
import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu
format = alu.bfloat
add = alu.bfloat_add
mult  = alu.bfloat_mult
format = alu.bfloat
def functional(input, input_s):
    output_array [format('0') for x in range (input_s)]
    sum = format('0')
    for  i in range (input_s):
        add(np.exp(input[i]),sum)
    for i in range (input_s):
        output_array[i] = np.exp(input[i])/sum
    return output_array
