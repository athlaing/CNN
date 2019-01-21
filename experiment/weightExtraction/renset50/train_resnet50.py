from pytorch.models import resnet50
from pytorch.utilities import GetDataSet
import torch.nn as nn
import torch
from torchvision.transforms import Compose, Normalize, Resize, ToTensor
from torch.optim import SGD
from torch.nn import BCELoss

normalize = Normalize([0.485, 0.456, 0.406],
                      [0.229, 0.224, 0.225])

test_dataset = GetDataSet('/home/samtruong/git/CNN-FPGA/parameter_extraction/renset50',
                                '/home/samtruong/git/CNN-FPGA/parameter_extraction/renset50/testList.txt',
                                transform=Compose([Resize(224), ToTensor(), normalize]))
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1)

model = resnet50(pretrained=True)
gt = torch.FloatTensor()
pred = torch.FloatTensor()
model.eval()
for inp, target in test_loader:
    target = torch.autograd.Variable(target)
    inp = torch.autograd.Variable(inp)
    out = model(inp)
    import IPython;IPython.embed()
    # Add results of the model's output to the aggregated prediction vector, and also add aggregated
    # ground truth information as well
    pred = torch.cat((pred, out.data), 0)
    gt = torch.cat((gt, target.data), 0)
