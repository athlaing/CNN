import csv
import torch
from os import listdir
from os.path import isfile, join

def loadRaw(param_path):
    files = [f for f in listdir(param_path) if isfile(join(param_path, f))]
    for i,file in enumerate(files,0):
        files[i] = param_path + '/' + file
    return files

def csv2tensor(rawFiles):
    package = {'convbias':None, 'fcweights':None,'convweights':None,'fcbias':None,}
    for i,file in enumerate(rawFiles,0):
        with open(file) as f:
            csv_reader = csv.reader(f, delimiter=',')

            # conv biases
            if i == 0:
                # 1 row
                for row in csv_reader:
                    package['convbias'] = torch.FloatTensor([float(item) for item in row])
                    
            # fc biases
            if i == 3:
                tensor = []
                for row in csv_reader:
                    tensor.append([float(item) for item in row])
                package['fcbias'] = torch.FloatTensor(tensor).squeeze(1)
                    
            # conv weights
            if i == 2:
                # 1 row
                for row in csv_reader:
                    package['convweights'] = torch.FloatTensor([float(item) for item in row]).unsqueeze(1).unsqueeze(1).unsqueeze(1) 
                    
            # fc weights
            if i == 1:
                tensor = []
                for row in csv_reader:
                    tensor.append([float(item) for item in row])
                package['fcweights'] = torch.FloatTensor(tensor)
    return package

def saveProcessed(package,save_path):
    torch.save(package['convbias'],save_path + '/convbias')
    torch.save(package['fcweights'],save_path + '/fcweights')
    torch.save(package['convweights'],save_path + '/convweights')
    torch.save(package['fcbias'],save_path + '/fcbias')
    
if __name__== "__main__":
    rawFiles = loadRaw('./parameters/raw')
    package = csv2tensor(rawFiles)
    saveProcessed(package,'./parameters/pytorch_ready' )