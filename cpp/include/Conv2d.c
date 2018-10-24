#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "Conv2d.h"

int get_output_d(int input_d, int filter_d, int padding, int stride) {
  int padded_input_d = input_d + padding * 2;
  return (padded_input_d - filter_d) / stride + 1;
}

float* zero_padding(float* input, int input_d, int padding) {
  if(!(padding)) {
    return input;
  }
  int input_s = input_d * input_d;
  int padded_input_d = input_d + 2 * padding;
  int padded_input_s = padded_input_d * padded_input_d;
  float* padded_input = malloc(padded_input_s * sizeof(float));
  int input_count = 0, row_count = 0, padding_count = 0;

  for(int i = 0; i < padded_input_s; i++) {
    if(i < (padded_input_d * padding) + padding) {
      padded_input[i] = 0;
    }
    else {
      if(input_count < input_s) {
        if(row_count < input_d) {
          padded_input[i] = input[input_count];
          input_count++;
          row_count++;
        }
        else {
          padded_input[i] = 0;
          if(padding_count == (padding * 2) - 1) {
            row_count = 0;
            padding_count = 0;
          }
          else {
            padding_count++;
          }
        }
      }
      else {
        padded_input[i] = 0;
      }
    }
  }

  return padded_input;
}

float dotproduct_and_summation(float* input, int input_d, float* filter,
                               int filter_d, int filter_s, int start) {
  float sum = 0;
  int count = 0, offset = 0;

  for(int i = 0; i < filter_s; i++) {
    sum += input[start + offset] * filter[i];
    if(count == filter_d - 1) {
      count = 0;
      offset += input_d - filter_d + 1;
    }
    else {
      count++;
      offset++;
    }
  }

  return sum;
}

float* Conv2d(float* input, int input_d, float* filter, int filter_d, int stride,
            int padding) {
  int padded_input_d = input_d + 2 * padding;
  int filter_s = filter_d * filter_d;
  int num_hops = (padded_input_d - filter_d) / stride;
  int output_s = (num_hops + 1) * (num_hops + 1);
  float* padded_input = zero_padding(input, input_d, padding);
  float* output = malloc(output_s * sizeof(float));
  int output_idx = 0, start = 0, count = 0, row_count = 0;
  while(output_idx != output_s) {
    output[output_idx] = dotproduct_and_summation(padded_input, padded_input_d,
                                                  filter, filter_d, filter_s,
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
  if(padding){
    free(padded_input);
  }

  return output;
}
