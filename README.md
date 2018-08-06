# CNN
An Assortment of Convolutional Neural Networks

To run AlexNet:

```python resize.py {filename}```

```make alex_model```

```./model```

To run MNIST:

```make mnist_model```

```./model```

### Current Activity
* Sam: Build Alexnet with hdf5 automatized weight
* Arthur: Reboot repo, cleanup, filter for final codes.

### Past Activity
* Sam:
  * Implemented maxpooling layer.
  * Implemented fully connected layer.
  * Implemented batchnorm layer.
  * Connected different MNIST layers together.
  * Wrote parsers for parameters load.
  * Developed customizable ````pytorch```` model package.
  * Setup accuracy testing script for MNIST C implementation.
  * Built and extracted parameters from Resnet50 architecture
  * Built HDF5 file system.
* Arthur:
  * Implemented convolutional layer.
  * Built and extracted parameters from the MNIST architecture.
  * Connected different MNIST layers together.
  * Organized parameters files output.
  * Developed Pytorch MNIST model
  * Debugged weights migration to C code
  * Built inLayer() of Resnet50
  * Built BasicBlock() and Bottleneck() of Resnet50
  * Built Alexnet in ```C```.
