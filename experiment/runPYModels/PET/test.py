import torch
import torchvision
from torchvision.transforms import Compose, ToTensor
import torch.optim as optim
import torch.nn as nn
from model import PETmodel, loadParameters
from dataset import PETDataset
from IPython.display import clear_output

model = PETmodel()
model = loadParameters(model,'./parameters/pytorch_ready/')
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)
epoch = 1
error = 0
window = 10
transformation = Compose([ToTensor()])
testdata = PETDataset('/root/hostStorage/ML_FPGA_compton_PET/image_compton_small_module_1mm_pitch', transform=transformation)
testloader = torch.utils.data.DataLoader(testdata, batch_size=1)

for ep in range(epoch):
    for i, data in enumerate(testloader, 0):
        image, label = data
        output = model(image)
        position = torch.argmax(output)
        if position != label:
            error += 1
#         optimizer.zero_grad()        
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step() 
#         running_loss += loss.item()
        clear_output()
        print('Progress: %.3f percent'%(i/testdata.__len__() * 100))
#        if i % window == window - 1:
#             print('[%5d] loss: %.3f' %(i + 1, running_loss / window))
#             running_loss = 0.0
print('Finished Testing:')
print('Accuracy: ' + str((testdata.__len__() - error) / testdata.__len__() * 100))