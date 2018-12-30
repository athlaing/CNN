#include <stdio.h>
#include <math.h>
#include <iostream>

using namespace std;

float kernel(int kernel_size, float* input, float* weight) {
  int array_size = (kernel_size * kernel_size - 1) + (kernel_size * kernel_size);
  float* arr = new float[array_size]();
  for(int i = 0; i < kernel_size * kernel_size; i++) {
    arr[i] = input[i] * weight[i];
  }
  int s_add = ceil(log2(kernel_size * kernel_size)); // number of addition stages
  bool even = false;
  if ((kernel_size * kernel_size) % 2) {
    even = false;
  }
  else {
    even = true;
  }
  int num_add = (kernel_size * kernel_size) / 2;
  int read_index = 0;
  int write_index = kernel_size * kernel_size;
  for(int stage = 0; stage < s_add; stage++) {
    for(int i = 0; i < num_add; i++) {
      arr[write_index] = arr[read_index] + arr[read_index + 1];
      write_index++;
      read_index += 2;
    }
    if(stage == 0) {
      read_index += 1;
    }
    num_add /= 2;
  }
  if (!even) {
    arr[array_size - 1] = arr[array_size - 2] + arr[kernel_size * kernel_size - 1];
  }
  // if you dont want to print, you can comment out everything below until return
  int newline = kernel_size * kernel_size;
  int count = 0;
  for(int i = 0; i < (kernel_size * kernel_size - 1) + (kernel_size * kernel_size); i++) {
    if(count == newline) {
      cout << endl;
      newline /= 2;
      count = 0;
    }
    cout << arr[i] << " ";
    count++;
  }
  cout << endl;
  delete [] arr;
  return arr[array_size - 1];
}


int main() {
  float input[9];
  float weight[9];
  for(int i = 0; i < 9; i++) {
    input[i] = i;
    weight[i] = i;
  }
  float sum = kernel(3, input, weight);
  cout << sum << endl;
  return 0;
}
