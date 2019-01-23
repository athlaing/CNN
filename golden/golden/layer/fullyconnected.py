import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu
from golden.activation import relu

add = alu.bfloat_add
mult  = alu.bfloat_mult
format = alu.bfloat
relu = relu.functional

def fc(weight, weight_w, bias, bias_h, input, relu_f):
    output = [format('0') for i in range (bias_h)]
    for i in range(bias_h):
        output[i] = bias[i];
        for j in range(weight_w):
            output[i] = add(mult(weight[i * weight_w + j], input[j]), output[i])
        if(relu_f):
            output[i] = relu(output[i])
    return output
