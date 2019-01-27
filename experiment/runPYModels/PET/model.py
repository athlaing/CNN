import torch
import torchvision
import numpy as np
import torch.nn.functional as F
import torch.nn as nn
from os import listdir
from os.path import isfile, join

class PETmodel(nn.Module):
    def __init__(self):
        super(PETmodel, self).__init__()
        self.conv = nn.Conv2d(1,100,1)
        self.softmax = nn.Softmax(1)
        self.fc = nn.Linear(16*100,169)
    def forward(self, x):
        x = self.conv(x)
        x = F.relu(x)
        x = x.view(-1, 16 * 100)
        x = self.fc(x)
        x = self.softmax(x)
        return x
    
def loadParameters(model,param_path):
    files = [f for f in listdir(param_path) if isfile(join(param_path, f))]
    model.conv.bias = torch.load(files[0])
    model.conv.weights = torch.load(files[1])
    model.fc.bias = torch.load(files[2])
    model.fc.weights = torch.load(files[3])
    print ("Done loading!")
    return model