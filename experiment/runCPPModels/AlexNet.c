#include <stdio.h>
#include <stdlib.h>
#include "include/Conv2d.h"
#include "include/Maxpool.h"
#include "include/helper.h"
#include "include/Fc.h"
#include <string.h>
#include <time.h>
#include <math.h>

float** basicBlockPool(float** input,
					   int input_d,
					   float*** conv_weight,
					   int conv_weight_d,
					   float* conv_bias,
					   int conv_padding,
					   int conv_stride,
					   int input_ch,
					   int conv_ch,
					   int pool_d,
					   int pool_stride,
					   int pool_padding) {
  // receptive field area
  int conv_weight_s = conv_weight_d * conv_weight_d;
  // activation map dimension
  int conv_out_d = get_output_d(input_d, conv_weight_d, conv_padding, conv_stride);
  // activation map area
  int conv_out_s = conv_out_d * conv_out_d;
  // temporary holds the activation map for each filter
  float** conv_hold = malloc(input_ch * sizeof(float*));
  // holds activation maps for each filter + bias
  float** conv = malloc_2D(conv_ch, conv_out_s);
  float** pool = malloc(conv_ch * sizeof(float*));

  for(int filter = 0; filter < conv_ch; filter++) {
    for(int channel = 0; channel < input_ch; channel++) {
      conv_hold[channel] = Conv2d(input[channel], input_d, conv_weight[filter][channel],
                         conv_weight_d, conv_stride, conv_padding);
    } // convolve for each channel(RGB) value of pixel
    for(int element = 0; element < conv_out_s; element++) {
      conv[filter][element] = conv_bias[filter];
      for(int channel = 0; channel < input_ch; channel++) {
        conv[filter][element] += conv_hold[channel][element];
      } // add values from activation map to bias
    } // y = conv_weight[filter][channel] . input[channel] + bias
    for(int channel = 0; channel < input_ch; channel++) {
      free(conv_hold[channel]);
    } // frees all temporary activation map created by conv2d
    pool[filter] = Maxpool(conv[filter], conv_out_d, pool_d, pool_stride,
                           pool_padding);
  } // for each filter convolve -> add bias -> pool

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
  // Q: are the values saved in row format or column format
  /* pictures conversions
   * p0 p1 p2
   * p3 p4 p5
   * p6 p7 p8 */
  /* file format expectation:
   * R0 R1 R2 R3 ... Rn ... G0 G1 G2 G3... Gn... B0 B1 B2 B3... Bn ?
   * 2-D array expectation
   * R0 G0 B0
   * R1 G1 B1
   * .  .  .
   * R2 G2 B2  where each column is a channel ?*/
  // 50175: sqrt(50175) = 224 x 224 image , depth of 3 -> RGB?
  float** image = read_2D("image.txt", 3, 50176);
  // 121: sqrt(121) = 11 x 11 receptive field dimensions?
  // 3:   depth of filter ?
  // 64:  number of features ?
  float*** block0_w = read_3D("alex_data/block0_w.txt", 64, 3, 121);
  // bias array y = w*x + bias
  float* block0_b = read_1D("alex_data/block0_b.txt", 64);

  // nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
  // nn.ReLU(inplace=True),
  // nn.MaxPool2d(kernel_size=3, stride=2)

  float** block0 = basicBlockPool(image, 	// 2-d image from file
								  224,   	// image dimension
								  block0_w, // 3-d weight
								  11,	 	// receptive field/filter dimension
								  block0_b, // bias array
								  2, 		// padding value 
								  4,		// stride amount
								  3,		// input depth
								  64,		// number of filters/features
								  3,		// pool dimensions
								  2,		// pool stride
								  0);		// pool padding

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

  int index[3] = {0, 1000, 1000};
  float max[3] = {output[0], -1, -1};
  for(int class = 1; class < 1000; class++) {
    if(output[class] >= max[0]) {
      max[0] = output[class];
      index[0] = class;
    }
  }

  float sum = 0;
  for(int class = 0; class < 1000; class++) {
    output[class] -= max[0];
    output[class] = exp(output[class]);
    sum += output[class];
  }

  for(int class = 0; class < 1000; class++) {
    output[class] = output[class]/sum;
    if((class != index[0]) && (output[class] >= max[1])) {
      max[1] = output[class];
      index[1] = class;
    }
  }

  for(int i = 0; i < 1000; i++) {
    if((i != index[0]) && (i != index[1]) && (output[i] >= max[2])) {
      max[2] = output[i];
      index[2] = i;
    }
  }

  char class[1000][30];
  FILE * fp;
  fp = fopen ("alex_data/classes.txt", "rb");
  for(int i = 0; i < 1000; i++) {
    fscanf(fp, "%s\n", class[i]);
  }
  fclose(fp);
  free(output);
  printf("Top 3 Predictions\n");
  for(int i = 0; i < 3; i++) {
    printf("%d. \"%s\" with %.2f%% probability\n", i+1, class[index[i]],
           output[index[i]]*100);
  }
}

int main() {

  clock_t begin = clock();
  alexnet();
  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("Time Spent: %.2f seconds\n", time_spent);

  return 0;
}
