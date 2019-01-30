#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "Conv2d.h"

/* Activation map dimension equation
 * paddedDim = input + padding * 2;
 * actMapDim = floor((paddedDim - filterDim) / stride) + 1;
 ****************************************/
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
    } // add padding until first input index
    else {
      if(input_count < input_s) {
        if(row_count < input_d) {
          padded_input[i] = input[input_count];
          input_count++;
          row_count++;
        } // insert input value
        else {
          padded_input[i] = 0;
          if(padding_count == (padding * 2) - 1) {
            row_count = 0;
            padding_count = 0;
          } // reset to insert input values
          else {
            padding_count++;
          } // padding has been added
        } // add padding or reset to insert input values
      } // add remaining input values
      else {
        padded_input[i] = 0;
      } // add padding to remaining padded elements
    } // conditions to deeals with elements after initial padding
  } // for all elements in padded array insert input value or padding

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
    } // sets the index to calculate next row
    else {
      count++;
      offset++;
    } // sets index to calculate next element
  } // calculate  dotproduct_and_summation every filter element

  return sum;
}

float* Conv2d(float* input,		// 1 channel of input (50176)
			  int input_d,		// input dimension (224)
			  float* filter,  	// weights for 1 filter / 1 channel
			  int filter_d,		// dimension of filter
			  int stride,		// filter stride amount
			  int padding) {    // image padding to be added
  // dimension with added padding		  
  int padded_input_d = input_d + 2 * padding;
  // filter area
  int filter_s = filter_d * filter_d;
  int num_hops = (padded_input_d - filter_d) / stride;
  int output_s = (num_hops + 1) * (num_hops + 1);
  float* padded_input = zero_padding(input, input_d, padding);
  // activation map
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
    } // moves filter downwares also resets filter to the left
    else {
      count++;
      start += stride;
    } // moves the filter side- ways to right
    output_idx++;
  } // calculate activation map values until no more hops
  if(padding){
    free(padded_input);
  }

  return output;
}
