import torch
import torchvision
from torchvision.transforms import Compose, ToTensor, Normalize
import torch.optim as optim
import torch.nn as nn
import matplotlib.pyplot as plt
import argparse
from visdom import Visdom

#===============================================================================
# Global Variables
#===============================================================================

DEFAULT_PORT = 8888
DEFAULT_HOSTNAME = "http://localhost"
EPOCH = 10
BATCHSIZE = 128
WINDOW = 100
LOSSES = []

#===============================================================================
# Flag Setup
#===============================================================================

parser = argparse.ArgumentParser(description='visualization arguments')
parser.add_argument('-port', metavar='port', type=int, default=DEFAULT_PORT,
                    help='port the visdom server is running on.')
parser.add_argument('-server', metavar='server', type=str,
                    default=DEFAULT_HOSTNAME,
                    help='Server address of the target to run the demo on.')

parser.add_argument('-name', metavar='name', type=str, default="PET", help='Name of Model')
FLAGS = parser.parse_args()

if (FLAGS.name == 'PET'):
    from PET.model import PETmodel, loadParameters, preprocess
    from PET.dataset import PETDataset
else:
    print("ERROR: Model not implemented")
    exit()

try:
    viz = Visdom(port=FLAGS.port, server=FLAGS.server)

    assert viz.check_connection(timeout_seconds=3), \
        'No connection could be formed quickly'
except BaseException as e:
    print(
        "The visdom experienced an exception while running: {}\n"
        "The demo displays up-to-date functionality with the GitHub version, "
        "which may not yet be pushed to pip. Please upgrade using "
        "`pip install -e .` or `easy_install .`\n"
        "If this does not resolve the problem, please open an issue on "
        "our GitHub.".format(repr(e))
    )
#===============================================================================
# Model Setup
#===============================================================================

cuda_predicate = torch.cuda.is_available()

criterion = nn.CrossEntropyLoss()
transformation = Compose([ToTensor(),Normalize(mean=[0.2916],std=[0.2589])])

model = None
if (cuda_predicate == True) :
    print("USING GPU")
    model = PETmodel().cuda()
else :
    print("USING CPU")
    model = PETmodel()

optimizer = optim.Adam(model.parameters(), lr=0.01)

test_data = PETDataset('D:/ML_FPGA_compton_PET/image_compton_small_module_1mm_pitch', transform=transformation, test=True, test_percentage=0.3)
train_data = PETDataset('D:/ML_FPGA_compton_PET/image_compton_small_module_1mm_pitch', transform=transformation, test=False, test_percentage=0.3)

test_loader = torch.utils.data.DataLoader(test_data, batch_size=BATCHSIZE, shuffle=False)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=BATCHSIZE, shuffle=True)

#===============================================================================
# Training Phase
#===============================================================================
for ep in range(EPOCH):
    for i, data in enumerate(train_loader, 0):
        image, label = data
        if (cuda_predicate == True) :
            image = image.cuda()
            label = label.cuda()
        output = model(image)
        optimizer.zero_grad()
        loss = criterion(output, label)
        loss.backward()
        optimizer.step()
        print("Batch Num:",i)
        if i % WINDOW == WINDOW - 1:
            torch.save(model,'./current_model')
            print(loss.item())
            LOSSES.append(loss.item())
            plt.plot(LOSSES)
            viz.matplot(plt,win="loss")


#===============================================================================
# Testing Phase
#===============================================================================
correct = 0
with torch.no_grad():
    for image, label in test_loader:
        if (cuda_predicate == True) :
            image = image.cuda()
            label = label.cuda()
        output = model(image)
        pred = output.max(1, keepdim=True)[1]
        correct += pred.eq(label.view_as(pred)).sum().item()
print ("Accuracy: ", correct)
