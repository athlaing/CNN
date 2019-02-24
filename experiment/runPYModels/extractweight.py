import torch
import torchvision
import numpy as np
import codecs, json
model = torch.load('current_model')
save_path = input('where to save the files: ')
for name, param in model.named_parameters():
        matrix = param.data.cpu().numpy()
        list  = matrix.tolist()
        file_path = save_path + str(name) + '.json'
        json.dump(list, codecs.open(file_path, 'w', encoding='utf-8'),
        separators=(',',':'), sort_keys=True, indent=4)
