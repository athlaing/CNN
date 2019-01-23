import sys
import json
from pprint import pprint
sys.path.append("../../")
import golden.layer.convolution.conv2D as conv2D
import golden.layer.fullyconnected.fc as fc
from golden.utils import loadMatrix as lm
from golden.activation import softmax.functional as softmax

#==========================================================# Internal Function
#==========================================================

def preprocess(weight_json):
    with open(input_json) as f:
        weights = json.load(f)
    #TODO===============
    # check model specific weights exists in json.
    #end TODO============
    return weights

def postprocess(output,out_json, ref_json):
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

def model(input):
    #TODO===============
    #  define specific model
    x = conv2D(input)
    x = fc(x)
    out = softmax(x)
    return out
    #end TODO============
