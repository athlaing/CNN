import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu
format = alu.bfloat

def relu_(input):
    if (input.sign == 0):
        return input
    else:
        return format('0'*16)

def functional(input):
    return list(map(relu_,input))
