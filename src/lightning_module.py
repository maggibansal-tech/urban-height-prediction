
import pytorch_lightning as pl
import torch
from torch import nn
from src.models.unet import UNet
from src.utils.metrics import rmse, mae

class HeightModel(pl.LightningModule):

    def __init__(self, cfg):
        super().__init__()
        self.save_hyperparameters(cfg)
        self.model = UNet()
        self.lr = cfg.training.lr
        self.criterion = nn.MSELoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        val_rmse = rmse(y_hat, y)
        val_mae = mae(y_hat, y)
        self.log("val_rmse", val_rmse, prog_bar=True)
        self.log("val_mae", val_mae, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)
