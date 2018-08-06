import sys
from PIL import Image
from  torchvision.transforms import ToTensor
from  torchvision.transforms import Normalize
import numpy as np
img = Image.open((sys.argv)[1])
img = img.resize((224,224), Image.ANTIALIAS)
totensor = ToTensor()
norm     = Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
img = totensor(img)
img = norm(img)
img = img.detach().numpy()
np.savetxt("image.txt",img.reshape(img.size),fmt="%f")
