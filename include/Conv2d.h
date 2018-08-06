#ifndef CONV2D
#define CONV2D

void fprint_array(float* input, int row_size);

float* zero_padding(float* input, int input_d, int padding);

float dotproduct_and_summation(float* input, int input_d, float* filter,
                               int filter_d, int filter_s, int start);

float* Conv2d(float* input, int input_d, float* filter, int filter_d, int stride,
              int padding);

int get_output_d(int input_d, int filter_d, int padding, int stride);

#endif
