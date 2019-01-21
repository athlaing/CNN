import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu

adder = alu.bfloat_mult
mult  = alu.bfloat_add
format = alu.bfloat

#=========================================================================
#Private functions
#=========================================================================
def get_output_d (input_d, filter_d, padding, stride):
    padded_input_d = input_d + padding * 2
    return (padded_input_d - filter_d) / stride + 1

def zero_padding(input, input_d, padding):
    if (padding != 0):
        return input
    input_s = input_d ** 2
    padded_input_d = input_d + 2 * padding
    padded_input_s = padded_input_d * padded_input_d
    padded_input = [0 for i in range(padded_input_s)]
    input_count = 0
    row_count = 0
    padding_count = 0

    for i in range(padded_input_s):
        if (i < (padded_input_d * padding) + padding):
            padded_input[i] = 0
        else:
            if (input_count < input_s):
                if (row_count < input_d):
                    padded_input[i] = input[input_count]
                    input_count += 1
                    row_count += 1
                else:
                    padded_input[i] = 0
                    if(padding_count == (padding * 2) - 1):
                        row_count = 0
                        padding_count =0
                    else:
                        padding_count += 1
            else:
                padded_input[i] = 0
    return padded_input

def dotproduct_and_summation(input, input_d, filter, filter_d, filter_s, start):
    sum = 0
    count = 0
    offset = 0

    for i in range(filter_s):
        sum += input[start + offset] * filter[i]
        if(count == filter_d - 1):
            count = 0
            offset += input_d - filter_d + 1
        else:
            count += 1
            offset += 1
    return sum
#=========================================================================
#Public function
#=========================================================================
def conv2D(input, input_d, filter, filter_d, stride = 0, padding = 0):
    padded_input_d = input_d + 2 * padding
    filter_s = filter_d * filter_d
    num_hops = (padded_input_d - filter_d) / stride
    output_s = (num_hops + 1) ** 2
    padded_intput = zero_padding(input, input_d, padding)
    output_idx = 0
    start = 0
    count = 0
    row_count = 0
    output = []

    while (output_idx != output_s):
        output.append(dotproduct_and_summation(padded_input,
                                               padding_input_d,
                                               filter,
                                               filter_d,
                                               filter_s,
                                               start))
        if (count == num_hops):
            count = 0
            row_count += 1
            start = row_count * stride * padded_input_d
        else:
            count += 1
            start += stride
        output_idx += 1
    return output
