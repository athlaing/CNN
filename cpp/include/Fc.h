#ifndef FC
#define FC
/*******************************************************************************
 *PUBLIC FACING API
 ******************************************************************************/
 float* Fc(
             float* weight,
             int weight_w,
             float* bias,
             int bias_h,
             float* input,
             int relu_f
           );
#endif
