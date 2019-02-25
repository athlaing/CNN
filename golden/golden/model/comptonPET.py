import sys
import json
import codecs
import numpy as np
import random as rd
from datetime import dateime
from pprint import pprint
from os import listdir
from os.path import isfile, join
sys.path.append("../../")
from golden.layer.convolution import conv2D as conv2D
from golden.layer.fullyconnected import fc as fc
from golden.utils import loadMatrix as lm
from golden.activation.softmax import functional as softmax
from golden.basic_logic.addmult_v2 import f2bfloat
from PIL import Image

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
    #TODO===============
    # Store model output in json and compare...
    # with reference
    #end TODO============
    pass

def streamInput(image_path, samplesize=1, shuffle=True):
    if (shuffle is True):
        rd.seed(datetime.now())

    # onlyfiles = [f for f in listdir(image_path)]
    # images = []
    for i in range(samplesize):
        image_name = image_path + '/' + onlyfiles[i]
        img = Image.open(image_name)
        arr = numpy.array(img)
        tup = tuple(arr, onlyfiles[i])
        images.append(tup)
    return images

def model(image):
    #TODO===============
    #  define specific model
    x = conv2D(image)
    x = fc(x)
    out = softmax(x)
    return out
    #end TODO============
