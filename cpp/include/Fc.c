#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "Fc.h"
#include "helper.h"
 /**************************************************************************
 *PUBLIC FACING API
 **************************************************************************/
float* Fc(
            float* weight,
            int weight_w,
            float* bias,
            int bias_h, // bias_w = 1
            float* input,
            int relu_f
          )
{
  float* output = malloc(sizeof(float) * bias_h);

  for(int i = 0; i < bias_h; i++){
    output[i] = bias[i];
    for(int j = 0; j < weight_w; j++){
      output[i] += weight[i * weight_w + j] * input[j];
    }
    if(relu_f) {
      output[i] = relu(output[i]);
    }
  }
  free(input);
  free(weight);
  free(bias);
  return output;
}
