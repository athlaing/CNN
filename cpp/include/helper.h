#ifndef HELPER
#define HELPER

void fprint_array(float* input, int row_size);

float*** malloc_3D(int x, int y, int z);

float** malloc_2D(int x, int y);

float* read_1D(char* path_name, int x);

float** read_2D(char* path_name, int x, int y);

float*** read_3D(char* path_name, int x, int y, int z);

float relu(float input);

void free_2D(float ** input, int x);

void free_3D(float *** input, int x, int y);

#endif
