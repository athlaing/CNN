#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "helper.h"

void free_2D(float ** input, int x) {
  for(int i = 0; i < x; i++) {
    free(input[i]);
  }
  free(input);
}

void free_3D(float *** input, int x, int y) {
  for(int i = 0; i < x; i++) {
    for(int j = 0; j < y; j++) {
      free(input[i][j]);
    }
    free(input[i]);
  }
  free(input);
}

void fprint_array(float* input, int row_size) {
  int count = 0;
  for(int i = 0; i < row_size * row_size; i++) {
    printf("%.2f ", input[i]);
    count++;
    if(!(count % row_size)) {
      printf("\n");
    }
  }
}

float*** malloc_3D(int x, int y, int z) {
  float*** output = malloc(sizeof(float**) * x);
  for(int i = 0; i < x; i++){
    output[i] = malloc(sizeof(float*) * y);
    for(int j = 0; j < y; j++){
      output[i][j] = malloc(sizeof(float) * z);
    }
  }
  return output;
}

float** malloc_2D(int x, int y) {
  float** output = malloc(sizeof(float**) * x);
  for(int i = 0; i < x; i++){
    output[i] = malloc(sizeof(float*) * y);
  }
  return output;
}

float* read_1D(char* path_name, int x) {
  FILE* fin = fopen(path_name, "rb");
  float* output = malloc(sizeof(float) * x);
  for(int i = 0; i < x; i++){
    fscanf(fin,"%f\n",&output[i]);
  }
  fclose(fin);
  return output;
}

float** read_2D(char* path_name, int x, int y) {
  FILE* fin = fopen(path_name, "rb");
  float** output = malloc(sizeof(float *) * x);
  for(int i = 0; i < x; i++){
    output[i] = malloc(sizeof(float) * y);
    for(int j = 0; j < y; j++){
      fscanf(fin,"%f\n", &output[i][j]);
    }
  }
  fclose(fin);
  return output;
}

float*** read_3D(char* path_name, int x, int y, int z) {
  FILE* fin = fopen(path_name, "rb");
  float*** output = malloc(sizeof(float **) * x);
  for(int i = 0; i < x; i++){
    output[i] = malloc(sizeof(float *) * y);
    for(int j = 0; j < y; j++){
      output[i][j] = malloc(sizeof(float) * z);
      for(int k = 0; k < z; k++){
        fscanf(fin,"%f\n", &output[i][j][k]);
      }
    }
  }
  fclose(fin);
  return output;
}

float relu(float input) {
  if(input > 0) {
    return input;
  }
  else {
    return 0;
  }
}
