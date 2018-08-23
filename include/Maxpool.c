#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "Maxpool.h"
#include "Conv2d.h"

float* Maxpool(float* input, int input_d, int filter_d, int stride,
               int padding) {
  int padded_input_d = input_d + 2 * padding;
  int filter_s = filter_d * filter_d;
  int num_hops = (padded_input_d - filter_d) / stride;
  int output_s = (num_hops + 1) * (num_hops + 1);
  float* padded_input = zero_padding(input, input_d, padding);
  float* output = malloc(output_s * sizeof(float));
  int output_idx = 0, start = 0, count = 0, row_count = 0;
  while(output_idx != output_s) {
    output[output_idx] = get_max(padded_input, padded_input_d, filter_d, filter_s,
                                 start);
    if(count == num_hops) {
      count = 0;
      row_count++;
      start = row_count * stride * padded_input_d;
    }
    else {
      count++;
      start += stride;
    }
    output_idx++;
  }
  free(padded_input);

  return output;
}

float get_max(float* input, int input_d, int filter_d, int filter_s, int start) {
  float output = input[start];
  int count = 0, offset = 0;

  for(int i = 0; i < filter_s - 1; i++) {
    if(count == filter_d - 1) {
      count = 0;
      offset += input_d - filter_d + 1;
    }
    else {
      count++;
      offset++;
    }
    if(input[start + offset] > output) {
      output = input[start + offset];
    }
  }
  if(output < 0) {
    return 0;
  }
  else {
    return output;
  }
}
