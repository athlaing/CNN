import itertools
import argparse
import numpy as np
from os import sys
sys.path.append("../..")
from golden.utils import face
from tqdm import tqdm

MODEL = None
INPUT = None
WEIGHT = None
MATLAB = None
PACKAGE = None
EPOCH = 1
ERROR = 0
ELAPSE = 0.0
TESTSIZE = 10000

def init():
    global MODEL
    global INPUT
    global WEIGHT
    global MATLAB
    global QUIET
    global PACKAGE

    parser = argparse.ArgumentParser(description='Run golden model of neural neworks with bfloat16 ALU')
    parser.add_argument('-n','--name', help='file name of the model', default=None)
    parser.add_argument('-d', '--data', help='path to images', default=None)
    parser.add_argument('-w', '--weight', help='path to weights', default=None)
    parser.add_argument('-m', '--matlab', help='path to matlab comparison', default=None)
    parser.add_argument('-q', '--quiet', help='print more inferencing statistics', default="True")

    args = vars(parser.parse_args())

    MODEL = args['name']
    INPUT = args['data']
    WEIGHT = args['weight']
    MATLAB = args['matlab']
    QUIET = args['quiet'] == 'True'

    #==========================================================
    # Model Look Up - Need to manually add new models
    #==========================================================
    if MODEL == 'comptonPET':
        # from comptonPET import preprocess, postprocess, streamInput, model
        import comptonPET
        PACKAGE = comptonPET
    else:
        exit("ERROR: model not found!")
    #==========================================================
    # End Model Look Up
    #==========================================================

def inference():
    print("Inference Started")
    global ERROR
    global TESTSIZE
    # print("="*80)
    # print("\t\t\t\tInference started")
    # print("="*80)
    weights = PACKAGE.preprocess(WEIGHT)
    inputs   = PACKAGE.streamInput(INPUT,samplesize=TESTSIZE)
    # print("Weight names: ")
    # for keys, value in weights.items():
    #     print(keys)
    for data in tqdm(inputs):
        image = data[0]
        label = data[1]
        output = PACKAGE.model(image, weights)
        predicted = np.argmax(output)
        if (label != predicted):
            ERROR += 1
    print('\n')

def stats():
    global QUIET
    if (not QUIET):
        print("MODEL ACCURACY: " + str((TESTSIZE - ERROR)/TESTSIZE * 100) + ' %')
    pass

if __name__ == '__main__':

    face("Run Golden Model")
    init()
    # inference through architecture
    inference()
    # output statistics
    stats()
