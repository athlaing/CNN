#include <stdio.h>
#include <stdlib.h>
#include "include/Conv2d.h"
#include "include/Maxpool.h"
#include "include/helper.h"
#include "include/Fc.h"
#include <string.h>
#include <time.h>

float** basicBlockPool(float** input, int input_d, float*** conv_weight,
                   int conv_weight_d, float* conv_bias, int conv_padding,
                   int conv_stride, int input_ch, int conv_ch, int pool_d,
                   int pool_stride, int pool_padding) {

  int conv_weight_s = conv_weight_d * conv_weight_d;
  int conv_out_d = get_output_d(input_d, conv_weight_d, conv_padding, conv_stride);
  int conv_out_s = conv_out_d * conv_out_d;

  float** conv_hold = malloc(input_ch * sizeof(float*));
  float** conv = malloc_2D(conv_ch, conv_out_s);
  float** pool = malloc(conv_ch * sizeof(float*));

  for(int filter = 0; filter < conv_ch; filter++) {
    for(int channel = 0; channel < input_ch; channel++) {
      conv_hold[channel] = Conv2d(input[channel], input_d, conv_weight[filter][channel],
                         conv_weight_d, conv_stride, conv_padding);
    }
    for(int element = 0; element < conv_out_s; element++) {
      conv[filter][element] = conv_bias[filter];
      for(int channel = 0; channel < input_ch; channel++) {
        conv[filter][element] += conv_hold[channel][element];
      }
      conv[filter][element] = relu(conv[filter][element]);
    }
    for(int channel = 0; channel < input_ch; channel++) {
      free(conv_hold[channel]);
    }
    pool[filter] = Maxpool(conv[filter], conv_out_d, pool_d, pool_stride,
                           pool_padding);
  }

  free(conv_hold);
  free_2D(input, input_ch);
  free_3D(conv_weight, conv_ch, input_ch);
  free(conv_bias);
  return pool;
}


float** basicBlock(float** input, int input_d, float*** conv_weight,
                   int conv_weight_d, float* conv_bias, int conv_padding,
                   int conv_stride, int input_ch, int conv_ch, int pool_d,
                   int pool_stride, int pool_padding) {

  int conv_weight_s = conv_weight_d * conv_weight_d;
  int conv_out_d = get_output_d(input_d, conv_weight_d, conv_padding, conv_stride);
  int conv_out_s = conv_out_d * conv_out_d;

  float** conv_hold = malloc(input_ch * sizeof(float*));
  float** conv = malloc_2D(conv_ch, conv_out_s);

  for(int filter = 0; filter < conv_ch; filter++) {
    for(int channel = 0; channel < input_ch; channel++) {
      conv_hold[channel] = Conv2d(input[channel], input_d, conv_weight[filter][channel],
                         conv_weight_d, conv_stride, conv_padding);
    }
    for(int element = 0; element < conv_out_s; element++) {
      conv[filter][element] = conv_bias[filter];
      for(int channel = 0; channel < input_ch; channel++) {
        conv[filter][element] += conv_hold[channel][element];
      }
      conv[filter][element] = relu(conv[filter][element]);
    }
    for(int channel = 0; channel < input_ch; channel++) {
      free(conv_hold[channel]);
    }
  }

  free(conv_hold);
  free_2D(input, input_ch);
  free_3D(conv_weight, conv_ch, input_ch);
  free(conv_bias);
  return conv;
}

void alexnet() {

  float** image = read_2D("image.txt", 3, 50176);
  float*** block0_w = read_3D("alex_data/block0_w.txt", 64, 3, 121);
  float* block0_b = read_1D("alex_data/block0_b.txt", 64);

  // nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
  // nn.ReLU(inplace=True),
  // nn.MaxPool2d(kernel_size=3, stride=2)

  float** block0 = basicBlockPool(image, 224, block0_w, 11, block0_b, 2, 4, 3, 64,
                              3, 2, 0);

  // nn.Conv2d(64, 192, kernel_size=5, padding=2),
  // nn.ReLU(inplace=True),
  // nn.MaxPool2d(kernel_size=3, stride=2),

  float*** block1_w = read_3D("alex_data/block1_w.txt", 192, 64, 25);
  float* block1_b = read_1D("alex_data/block1_b.txt", 192);

  float** block1 = basicBlockPool(block0, 27, block1_w, 5, block1_b, 2, 1, 64, 192,
                              3, 2, 0);

  // nn.Conv2d(192, 384, kernel_size=3, padding=1),
  // nn.ReLU(inplace=True)

  float*** block2_w = read_3D("alex_data/block2_w.txt", 384, 192, 9);
  float* block2_b = read_1D("alex_data/block2_b.txt", 384);

  float** block2 = basicBlock(block1, 13, block2_w, 3, block2_b, 1, 1, 192, 384,
                              0, 0, 0);

  // nn.Conv2d(384, 256, kernel_size=3, padding=1),
  // nn.ReLU(inplace=True),

  float*** block3_w = read_3D("alex_data/block3_w.txt", 256, 384, 9);
  float* block3_b = read_1D("alex_data/block3_b.txt", 256);

  float** block3 = basicBlock(block2, 13, block3_w, 3, block3_b, 1, 1, 384, 256,
                              0, 0, 0);

  // nn.Conv2d(256, 256, kernel_size=3, padding=1),
  // nn.ReLU(inplace=True),
  // nn.MaxPool2d(kernel_size=3, stride=2)

  float*** block4_w = read_3D("alex_data/block4_w.txt", 256, 256, 9);
  float* block4_b = read_1D("alex_data/block4_b.txt", 256);

  float** block4 = basicBlockPool(block3, 13, block4_w, 3, block4_b, 1, 1, 256, 256,
                              3, 2, 0);

  float* block = malloc(9216 * sizeof(float));
  int count = 0;
  for(int i = 0; i < 256; i++) {
    for(int j = 0; j < 36; j++) {
      block[count] = block4[i][j];
      count++;
    }
  }
  free_2D(block4, 256);

  // nn.Dropout(),
  // nn.Linear(256 * 6 * 6, 4096),
  // nn.ReLU(inplace=True),

  float* linear0_w = read_1D("alex_data/linear0_w.txt", 37748736);
  float* linear0_b = read_1D("alex_data/linear0_b.txt", 4096);

  float* linear0 = Fc(linear0_w, 9216, linear0_b, 4096, block, 1);

  // nn.Dropout(),
  // nn.Linear(4096, 4096),
  // nn.ReLU(inplace=True),

  float* linear1_w = read_1D("alex_data/linear1_w.txt", 16777216);
  float* linear1_b = read_1D("alex_data/linear1_b.txt", 4096);

  float* linear1 = Fc(linear1_w, 4096, linear1_b, 4096, linear0, 1);

  // nn.Linear(4096, num_classes),

  float* linear2_w = read_1D("alex_data/linear2_w.txt", 4096000);
  float* linear2_b = read_1D("alex_data/linear2_b.txt", 1000);

  float* output = Fc(linear2_w, 4096, linear2_b, 1000, linear1, 0);

  float max = output[0];
  int index = 1000;
  for(int class = 0; class < 1000; class++) {
    if(output[class] >= max) {
      max = output[class];
      index = class;
    }
  }

  char class[80];
  FILE * fp;
  fp = fopen ("alex_data/classes.txt", "rb");
  for(int i = 0; i < 1000; i++) {
    fscanf(fp, "%s\n", class);
    if(i == index) {
      break;
    }
  }
  fclose(fp);
  free(output);
  printf("predicted = %s\n", class);
}

int main() {

  clock_t begin = clock();
  alexnet();
  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("Time Spent: %f\n", time_spent);

  return 0;
}
