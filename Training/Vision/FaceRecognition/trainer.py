import os
import random

from Training.training_constants import *
from Training.Vision.FaceRecognition.face_recognition_hyperparameters import *
from DataManagment.file_system import ensure_dir, save_to_file, load_file
from Training.DataPipeline.data_loader import get_train_test_sets
from Training.Vision.FaceRecognition.Models.siamese_network import SiameseNetwork
from Training.Vision.FaceRecognition.Models.inception_resnet import InceptionResnetNetwork
from Training.Extractors.index_extractor import IndexExtractor

import pytorch_lightning as pl
from pytorch_lightning import loggers
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import torch
from torchvision import transforms
from datetime import datetime
import wandb


def save_model_specs(path: Path, train_specs: dict):
    ensure_dir(path)
    save_to_file(train_specs, path / MODEL_INFO_FILE)


def load_model(path: Path):
    specs = load_file(path / MODEL_INFO_FILE)
    cur_model, input_extractor, output_extractor = initialize_model_pipeline(specs, False)
    checkpoint = torch.load(path / MODEL_CHECKPOINTS_FOLDER / f"{TOP_MODEL_NAME}.ckpt")
    cur_model.load_state_dict(checkpoint['state_dict'])
    return cur_model, input_extractor, output_extractor, specs


def initialize_model_pipeline(specs: dict, to_train: bool = True) -> tuple:
    model_data_path = MODELS_FOLDER / f"Model_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}"

    input_transformer = torch.nn.Sequential(transforms.Resize(INPUT_DIMENSIONS))

    model_architecture = InceptionResnetNetwork

    if to_train:
        cur_train_test_sets, evaluation_loader = get_train_test_sets(DATASETS.DIGI_FACE, input_transformer,
                                                                     use_cache=USE_CACHE,
                                                                     batch_size=specs["batch_size"],
                                                                     random_seed=specs["random_seed"],
                                                                     evaluation_df=specs["evaluation_set"])
        save_model_specs(model_data_path, specs)
    else:
        cur_train_test_sets = None
        evaluation_loader = None

    model = model_architecture(torch.nn.MSELoss(), torch.optim.Adam, cur_train_test_sets, specs)
    if to_train:
        ensure_dir(WANDB_FOLDER)
        wandb_logger = pl.loggers.WandbLogger(project=WANDB_PROJECT_NAME, name=model_data_path.name,
                                              save_dir=WANDB_FOLDER)
        wandb_logger.experiment.config.update(specs)

        checkpoint_callback = pl.callbacks.ModelCheckpoint(dirpath=model_data_path / MODEL_CHECKPOINTS_FOLDER,
                                                           save_top_k=1, monitor="val_acc", mode="max",
                                                           filename=TOP_MODEL_NAME)
        early_stopping_callback = EarlyStopping(monitor="val_loss", patience=specs["early_stopping_patience"],
                                                mode="min")
        accelerator = "gpu" if DEVICE == "cuda" else None
        trainer = pl.Trainer(accelerator=accelerator, devices=1, max_epochs=specs["epochs"], enable_progress_bar=True,
                             logger=wandb_logger, callbacks=[checkpoint_callback, early_stopping_callback])
        trainer.fit(model)

        # Evaluate the model
        trainer.test(model, dataloaders=evaluation_loader)

        wandb.finish()

    return model.to(DEVICE), input_transformer


def train(overwrite: dict = None):
    train_specs = {
        "description": "",
        "dataset_path": DATASETS.DIGI_FACE.name,
        "evaluation_set": EVALUATION_SAMPLES_DF.name,
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "learning_rate": LEARNING_RATE,
        "early_stopping_patience": EARLY_STOPPING_PATIENCE,
        "random_seed": random.randint(0, 100000),
        "input_dimensions": INPUT_DIMENSIONS,
        "features_dim": FEATURES_DIM,
        "grayscale": GRAYSCALE,
    }
    if overwrite is not None:
        train_specs.update(overwrite)
    print("Training specs:")
    print(train_specs)
    model, _, _ = initialize_model_pipeline(train_specs, True)


if __name__ == "__main__":
    train()
