#include <stdio.h>
#include <stdlib.h>
#include "include/Conv2d.h"
#include "include/Maxpool.h"
#include "include/helper.h"
#include "include/Fc.h"
#include <string.h>

float** basicBlock(float** input, int input_d, float*** conv_weight,
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
    pool[filter] = Maxpool(conv[filter], conv_out_d, pool_d,
                           pool_stride, pool_padding);
  }

  free(conv_hold);
  free_2D(input, input_ch);
  free_3D(conv_weight, conv_ch, input_ch);
  free(conv_bias);
  return pool;
}

void mnist() {

  float** image = read_2D("mnist_data/input", 1, 784);
  float*** block0_w = read_3D("mnist_data/conv1.weight", 32, 1, 25);
  float* block0_b = read_1D("mnist_data/conv1.bias", 32);

  //       h_conv1 = self.conv1(x)
  //       h_conv1_relu = F.relu(h_conv1)
  //       h_pool1 = self.pool(h_conv1_relu)
  //       self.conv1 = nn.Conv2d(1, 32, 5, stride = 1, padding = 2)

  float** block0 = basicBlock(image, 28, block0_w, 5, block0_b, 2, 1, 1, 32, 2,
                              2, 0);

  //       h_conv2 = self.conv2(h_pool1)
  //       h_conv2_relu = F.relu(h_conv2)
  //       h_pool2 = self.pool(h_conv2_relu)
  //       self.conv2 = nn.Conv2d(32, 64, 5, stride = 1, padding = 2)

  float*** block1_w = read_3D("mnist_data/conv2.weight", 64, 32, 25);
  float* block1_b = read_1D("mnist_data/conv2.bias", 64);

  float** block1 = basicBlock(block0, 14, block1_w, 5, block1_b, 2, 1, 32, 64, 2,
                              2, 0);

  //       h_pool2_flat = h_pool2.view(1, 64*7*7)

  float* block = malloc(3136* sizeof(float));
  int count = 0;
  for(int i = 0; i < 64; i++) {
    for(int j = 0; j < 49; j++) {
      block[count] = block1[i][j];
      count++;
    }
  }
  free_2D(block1, 64);

  //       h_fc1 = self.fc1(h_pool2_flat)
  //       h_fc1_relu = F.relu(h_fc1)

  float* linear0_w = read_1D("mnist_data/fc1.weight", 3211264);
  float* linear0_b = read_1D("mnist_data/fc1.bias", 1024);

  float* linear0 = Fc(linear0_w, 3136, linear0_b, 1024, block, 1);

  //       y_conv = self.fc2(h_fc1_drop)

  float* linear1_w = read_1D("mnist_data/fc2.weight", 10240);
  float* linear1_b = read_1D("mnist_data/fc2.bias", 10);

  float* output = Fc(linear1_w, 1024, linear1_b, 10, linear0, 0);

  float max = output[0];
  int max_index = 0;
  for(int i = 0; i < 10; i++) {
    if(output[i] > max) {
      max_index = i;
      max = output[i];
    }
  }

  printf("number = %d\n", max_index);
}

int main() {

  mnist();

  return 0;
}
