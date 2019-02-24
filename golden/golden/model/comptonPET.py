import sys
import json
import codecs
import numpy as np
from pprint import pprint
from os import listdir
from os.path import isfile, join
sys.path.append("../../")
from golden.layer.convolution import conv2D as conv2D
from golden.layer.fullyconnected import fc as fc
from golden.utils import loadMatrix as lm
from golden.activation.softmax import functional as softmax

#==========================================================
# Internal Function
#==========================================================

def preprocess(weight_path):
    onlyfiles = [f for f in listdir(weight_path)]
    weights = {}
    for file in onlyfiles:
        file_path = weight_path + '/' + str(file)
        with open(file_path) as f:
            obj = codecs.open(file_path, 'r', encoding='utf-8').read()
            list = json.loads(obj)
            weight = np.array(list)
            weights[str(file)] = weight
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

def model(image):
    #TODO===============
    #  define specific model
    x = conv2D(image)
    x = fc(x)
    out = softmax(x)
    return out
    #end TODO============
