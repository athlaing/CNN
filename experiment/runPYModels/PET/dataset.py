import torch
import torchvision
import os
import matplotlib.pyplot as plt
import random
import math
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

class PETDataset(Dataset):
    def __init__(self, path, transform=None, test=False, test_percentage=0, seed=0):
        random.seed(seed)
        self.transform = transform
        self.path = path
        self.data = []
        self.testdata = []
        self.traindata = []
        self.test_percentage = test_percentage
        self.test = test
        for i in range(1,170):
            
            if i < 10:
                labelname = '/00' + str(i)
            elif i >= 10 and i < 100:
                labelname = '/0' + str(i)
            else:
                labelname = '/' + str(i)
            folder = self.path + labelname + '/'
            for images in os.walk(folder):
                for image in images[2]:
                     (self.data).append((folder + image,i))     
                        
        random.shuffle(self.data)
        testsize = math.floor(test_percentage * len(self.data))
        self.testdata = self.data[0:testsize]
        self.traindata= self.data[testsize:-1]
                
    def __getitem__(self, index):
        label = None
        image = None
        
        if self.test is True:
            label = (self.testdata[index][1])
            image = Image.open((self.testdata[index])[0])
        if self.test is False:
            label = (self.traindata[index][1])
            image = Image.open((self.traindata[index])[0])
            
        if (self.transform is not None):
            image = self.transform(image)
        return (image, label - 1)
    
    def __len__(self):
        if self.test is True:
            return math.floor(len(self.data) * self.test_percentage)
        if self.test is False:
            return math.floor(len(self.data) * (1 - self.test_percentage))

    def showSample(self, index):
        image, label = self.__getitem__(index)
        plt.imshow(image)
        plt.show()
        print ("Label is: " + str(label))