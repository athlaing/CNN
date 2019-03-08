import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu
from golden.activation import relu

format = alu.bfloat

def fc(input, weight, bias):
    bias_d = len(bias)
    weight_d = len(weight)
    input_d = len(input)
    output = [format('0'*16) for i in range (bias_d)]

    # go from 0 to 169
    for i in range(bias_d):
        output[i] = bias[i];
        # go from 0 1600
        for j in range(int(weight_d / input_d)):
            output[i] += weight[i*input_d+j] * input[j]
    return output
