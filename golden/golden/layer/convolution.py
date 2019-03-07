import sys
sys.path.append("../../")
from golden.basic_logic import addmult_v2 as alu

format = alu.bfloat

#=========================================================================
#Private functions
#=========================================================================
def dotproduct_and_summation(padded_input, filter, start):
    num_filter = len(filter)
    # if each filter has more than 1 weight  (type = list)
    if (isinstance(filter[0], list)):
        filter_d = len(filter[0]) # all filters should have same length
    # if each filter is only 1 weight (type = bfloat)
    else:
        filter_d = 1;
    sum = format('0'*16)
    count = 0
    offset = 0

    for i in range(num_filter):
        for  j in range(filter_d):
            sum += padded_input[start+j] * filter[i]
    return sum

#=========================================================================
#Public functions
#=========================================================================
def conv1D(input, filter, stride = 1, padding = 0):

    input_d = len(input)
    num_filter = len(filter)

    # if each filter has more than 1 weight  (type = list)
    if (isinstance(filter[0], list)):
        filter_d = len(filter[0]) # all filters should have same length
    # if each filter is only 1 weight (type = bfloat)
    else:
        filter_d = 1;

    # If user doesnt specify padding, see if padding is needed
    # Assume that padding is always an odd number.
    if (padding == 0 and filter_d != 1):
         # padding is always an integer because filter_d is odds
        padding = (filter_d - 1) / 2

    # zero padding the input, if padding is 0 then there is no padding
    padded_input = [format('0'*16) for i in range(padding)]
    padded_input.extend(input)
    padded_input.extend([format('0'*16) for i in range(padding)])
    padded_input_d = len(padded_input)

    num_hops = (padded_input_d - filter_d) / stride # integer division

    output_idx = 0
    start = 0
    output = []

    while (output_idx < num_hops + 1):
        output.append(dotproduct_and_summation(padded_input, filter, start))
        start += stride
        output_idx += 1
    return output
