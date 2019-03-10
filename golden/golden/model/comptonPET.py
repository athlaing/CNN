import sys
import json
import codecs
import numpy as np
import random as rd
from tqdm import tqdm
from pprint import pprint
from os import listdir
from os.path import isfile, join
sys.path.append("../../")
from golden.layer.convolution import conv1D as conv1D
from golden.layer.fullyconnected import fc as fc
from golden.utils import loadMatrix as lm
from golden.activation.softmax import functional as softmax
from golden.activation.relu import functional as relu
from golden.basic_logic.addmult_v2 import f2bfloat
from PIL import Image

#==========================================================
# Internal Function
#==========================================================

def preprocess(weight_path):
    print("Loading Weights")
    onlyfiles = [f for f in listdir(weight_path)]
    weights = {}
    for file in tqdm(onlyfiles):
        file_path = weight_path + '/' + str(file)
        with open(file_path) as f:
            obj = codecs.open(file_path, 'r', encoding='utf-8').read()
            lst = json.loads(obj)
            weight = np.array(lst).flatten()
            weight = list(map(f2bfloat, weight))
            weights[str(file)] = weight
    print('\n')
    return weights

def postprocess(output,out_json, ref_json):
    #TODO===============
    # Store model output in json and compare...
    # with reference
    #end TODO============
    pass

def streamInput(image_path, samplesize=1):
    print("Loading Images")
    data = []
    for i in tqdm(range(samplesize)):
        label = rd.randint(1,169)
        labelname = None;
        if label < 10:
            labelname = '/00' + str(label)
        elif label >= 10 and label < 100:
            labelname = '/0' + str(label)
        else:
            labelname = '/' + str(label)
        folder = image_path  + labelname + '/'
        onlyfiles = [f for f in listdir(folder)]
        sample_image = onlyfiles[rd.randint(0, len(onlyfiles) - 1)]
        img = Image.open(folder + sample_image)
        arr = np.array(img).tolist()[0]
        arr = list(map(f2bfloat,arr))
        tup = (arr, label)
        data.append(tup)
    print('\n')
    return data

def model(image, weights):
    #TODO===============
    #  define specific model
    x = conv1D(image,
        weights['conv.weight.json'],
        weights['conv.bias.json'])
    x = relu(x)
    x = fc(x,
        weights['fc.weight.json'],
        weights['fc.bias.json'])
    out = softmax(x)
    return out
    #end TODO============
