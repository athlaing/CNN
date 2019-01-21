import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms
import multiprocessing
import os

class GetDataSet(Dataset):
    def __init__(self, data_dir, image_list_file, is_preprocessed=False, transform=None, convert_to='RGB'):

        image_names = []
        labels = []
        with open(image_list_file, "r") as f:
            for line in f:
                items = line.split()
                image_name= items[0]
                label = items[1:]
                label = [int(i) for i in label]
                image_name = os.path.join(data_dir, image_name)
                image_names.append(image_name)
                labels.append(label)

        self.image_names = image_names
        self.labels = labels
        self.transform = transform
        self.convert_to = convert_to
        self.is_preprocessed = is_preprocessed

    def __getitem__(self, index):

        image_name = self.image_names[index]
        label = self.labels[index]
        if self.transform and not self.is_preprocessed:
            image = Image.open(image_name).convert(self.convert_to)
            image = self.transform(image)
        else:
            image = torch.load(image_name)
        return image, torch.FloatTensor(label)

    def __len__(self):
        return len(self.image_names)
