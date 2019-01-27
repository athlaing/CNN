import torch
import torchvision
import os
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

class PETDataset(Dataset):
    def __init__(self, path, transform=None):
        self.transform = transform
        self.path = path
        self.data = []
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
    def __getitem__(self, index):
        label = (self.data[index][1])
        image = Image.open((self.data[index])[0])
        if (self.transform is not None):
            image = self.transform(image)
        return (image, label)
    
    def __len__(self):
        return len(self.data)

    def showSample(self, index):
        image, label = self.__getitem__(index)
        plt.imshow(image)
        plt.show()
        print ("Label is: " + str(label))