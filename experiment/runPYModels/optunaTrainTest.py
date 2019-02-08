import torch
import torchvision
from torchvision.transforms import Compose, ToTensor, Normalize
import torch.optim as optim
import torch.nn as nn
from model import PETmodel, loadParameters, preprocess
from dataset import PETDataset
import optuna
optuna.logging.disable_default_handler()
from tqdm import tqdm_notebook as tqdm
EPOCH = 10
BATCHSIZE = 128
WINDOW = 100

# model = PETmodel()
# model = loadParameters(model,'./parameters/pytorch_ready/')
# model = torch.load('current_model')
criterion = nn.CrossEntropyLoss()
transformation = Compose([ToTensor(),Normalize(mean=[0.2916],std=[0.2589])])

test_data = PETDataset('D:/ML_FPGA_compton_PET/image_compton_small_module_1mm_pitch', transform=transformation, test=True, test_percentage=0.3)
train_data = PETDataset('D:/ML_FPGA_compton_PET/image_compton_small_module_1mm_pitch', transform=transformation, test=False, test_percentage=0.3)

test_loader = torch.utils.data.DataLoader(test_data, batch_size=BATCHSIZE, shuffle=False)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=BATCHSIZE, shuffle=True)

cuda_predicate = torch.cuda.is_available()

# mean, std = preprocess(testloader)
# print("Mean:" + str(mean))
# print("STD: " + str(std))

def train(model, train_loader, optimizer):
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
        if i % WINDOW == WINDOW - 1:
            torch.save(model,'./current_model')

def test(model, device, test_loader):
    correct = 0
    with torch.no_grad():
        for image, label in test_loader:
            if (cuda_predicate == True) :
                image = image.cuda()
                label = label.cuda()
            output = model(image)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(label.view_as(pred)).sum().item()

    return 1 - correct / len(test_loader.dataset)

def get_optimizer(trial, model):
    optimizer_names = ['Adam', 'MomentumSGD']
    optimizer_name = trial.suggest_categorical('optimizer', optimizer_names)
    weight_decay = trial.suggest_loguniform('weight_decay', 1e-10, 1e-3)
    if optimizer_name == optimizer_names[0]:
        adam_lr = trial.suggest_loguniform('adam_lr', 1e-5, 1e-1)
        optimizer = optim.Adam(model.parameters(), lr=adam_lr, weight_decay=weight_decay)
    else:
        momentum_sgd_lr = trial.suggest_loguniform('momentum_sgd_lr', 1e-5, 1e-1)
        optimizer = optim.SGD(model.parameters(), lr=momentum_sgd_lr,
                              momentum=0.9, weight_decay=weight_decay)
    return optimizer

def objective_wrapper(pbar):
    def objective(trial):
        model = None
        if (cuda_predicate == True) :
            print("USING GPU")
            model = PETmodel().cuda()
        else :
            print("USING CPU")
            model = PETmodel()
        optimizer = get_optimizer(trial, model)
        for step in range(EPOCH):
            train(model, train_loader, optimizer)
            error_rate = test(model, test_loader)

            trial.report(error_rate, step)
            if trial.should_prune(step):
                pbar.update()
                raise optuna.structs.TrialPruned()

        pbar.update()

        return error_rate

    return objective


if __name__== "__main__":
    TRIAL_SIZE = 100
    with tqdm(total=TRIAL_SIZE) as pbar:
        study = optuna.create_study(pruner=optuna.pruners.MedianPruner())
        study.optimize(objective_wrapper(pbar), n_trials=TRIAL_SIZE)

    study.best_params
    study.best_value
    study.trials[0]
    df = study.trials_dataframe()
    df.head()
    df.to_csv('./result.csv')
    torch.save(model, './final_model')
