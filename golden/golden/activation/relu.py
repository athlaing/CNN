import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu
format = alu.bfloat
def functional(input):
    if (input.sign == 0):
        return input
    else:
        return format('0')
