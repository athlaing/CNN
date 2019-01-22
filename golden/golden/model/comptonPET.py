import sys
sys.path.append("../../")
from golden.convolutional import convolution
from golden.fully_connected import fc
from golden.utils import loadMatrix as lm
conv2D = convolution.conv2D
fc = fc.fc
