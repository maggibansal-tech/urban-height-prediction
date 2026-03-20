
import hydra
from omegaconf import DictConfig
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from src.lightning_module import HeightModel
from src.data.datamodule import HeightDataModule
from src.utils.seed import seed_everything

@hydra.main(config_path="../configs", config_name="london_single", version_base=None)
def main(cfg: DictConfig):

    seed_everything(cfg.training.seed)

    model = HeightModel(cfg)
    datamodule = HeightDataModule(cfg)

    checkpoint_callback = ModelCheckpoint(
        dirpath="checkpoints/",
        filename="best-{epoch}-{val_rmse:.3f}",
        monitor="val_rmse",
        mode="min",
        save_top_k=1
    )

    trainer = Trainer(
        max_epochs=cfg.training.epochs,
        deterministic=True,
        callbacks=[checkpoint_callback],
        accelerator="cpu"
    )

    trainer.fit(model, datamodule=datamodule)

if __name__ == "__main__":
    main()
