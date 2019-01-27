import torch
import torchvision
from torchvision.transforms import Compose, ToTensor
import torch.optim as optim
import torch.nn as nn
from model import PETmodel
from dataset import PETDataset

model = PETmodel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)
epoch = 1
running_loss = 0.0
window = 10
transformation = Compose([ToTensor()])
traindata = PETDataset('/root/hostStorage/ML_FPGA_compton_PET/image_compton_small_module_1mm_pitch', transform=transformation)
trainloader = torch.utils.data.DataLoader(traindata, batch_size=16)

for ep in range(epoch):
    for i, data in enumerate(trainloader, 0):
        images, labels = data
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        if i % window == window - 1:
            print('[%5d] loss: %.3f' %(i + 1, running_loss / window))
            running_loss = 0.0
print('Finished Training')    