import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu

format = alu.bfloat

#=========================================================================
#Private functions
#=========================================================================

#=========================================================================
#Public functions
#=========================================================================
def conv1D(input, weights, biases, stride = 1, padding = 0):

    input_len = len(input)
    num_feature_map = len(weights)

    # if each weights has more than 1 weights  (type = list)
    if (isinstance(weights[0], list)):
        kernel_size = len(weights[0]) # all weights should have same length
    # if each weights is only 1 weights (type = bfloat)
    else:
        kernel_size = 1;

    # If user doesnt specify padding, see if padding is needed
    # Assume that padding is always an odd number.
    if (padding == 0 and kernel_size != 1):
         # padding is always an integer because kernel_size is odds
        padding = (kernel_size - 1) / 2

    # zero padding the input, if padding is 0 then there is no padding
    # aray looks like 000xxxxxxxxxxxxxxxxxx000 where x is data, if padding = 3
    padded_input = [format('0'*16) for i in range(padding)]
    padded_input.extend(input)
    padded_input.extend([format('0'*16) for i in range(padding)])
    padded_input_len = len(padded_input)

    num_hops = int((padded_input_len - kernel_size) / stride )# integer division
    output_col = num_hops + 1
    output_row = num_feature_map
    output = []

    # for each channel
    for r in range(output_row):
        bias = biases[r]
        weight = weights[r]
        start = 0
        for c in range(output_col):
            sum = bias

            # General Case where the kerenl is a list of bfloat 16 (iterable)
            if kernel_size != 1:
                for element_id, element in enumerate(weight):
                    sum += padded_input[start + element_id] * element
            # Case where the kernel is just a bfloat16
            elif kernel_size == 1:
                sum += padded_input[start] * weight

            output.append(sum)
            start += stride
    return output
