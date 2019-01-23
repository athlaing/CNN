import sys
import json
from pprint import pprint
sys.path.append("../../")
from golden.convolutional import convolution
from golden.fully_connected import fc
from golden.utils import loadMatrix as lm
conv2D = convolution.conv2D
fc = fc.fc

#==========================================================# Internal Function
#==========================================================

def preprocess(weight_json):
    with open(input_json) as f:
        weights = json.load(f)
    #TODO===============
    # check model specific weights exists in json.
    #end TODO============
    return weights

def postprocess(out_json, ref_json):
    with open(ref_json) as f:
        ref = json.load(f)
    #TODO===============
    # Store model output in json and compare...
    # with reference
    #end TODO============

def streamInput(in_path, batchsize=1):
    #TODO===============
    # take in  a batch of input for processing.
    #end TODO============
    pass

def model():
    #TODO===============
    #  define specific model
    #end TODO============
