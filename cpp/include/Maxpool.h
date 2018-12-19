#ifndef MAX_POOLING
#define MAX_POOLING

/*******************************************************************************
 *HELPER FUCTIONS
 ******************************************************************************/
void p_get_anchor_pixel(
                      int** anchor_pixel,
                      int*num_anchor_pixel,
                      int input_dim,
                      int filter_dim,
                      int stride,
                      float** output
                    );

void p_get_output(
                int* anchor_pixel,
                float* input,
                float* output,
                int num_anchor_pixel,
                int filter_dim,
                int input_dim
              );
/*******************************************************************************
 *PUBLIC FACING API
 ******************************************************************************/

// float* Maxpool(float* input, int input_dim, int filter_dim, int stride,
//                int padding);

float* Maxpool(float* input, int input_d, int filter_d, int stride, int padding);

float get_max(float* input, int input_d, int filter_d, int filter_s, int start);

#endif
