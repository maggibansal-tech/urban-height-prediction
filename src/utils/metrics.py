
import torch
from sklearn.metrics import r2_score

def rmse(pred, target):
    return torch.sqrt(torch.mean((pred - target) ** 2))

def mae(pred, target):
    return torch.mean(torch.abs(pred - target))

def relative_rmse(pred, target):
    return rmse(pred, target) / torch.mean(target)

def r2(pred, target):
    return r2_score(
        target.detach().cpu().numpy().flatten(),
        pred.detach().cpu().numpy().flatten()
    )
