from Training.training_constants import *
from Training.Vision.FaceRecognition.dataset import SiameseDataset
from Training.Extractors.index_extractor import IndexExtractor

from torch.utils.data import DataLoader
import random


def get_train_test_sets(dataset_path: Path, input_transformer,
                        use_cache: bool, batch_size: int, random_seed: int, evaluation_df: Path):
    train_set = SiameseDataset(dataset_path, input_transformer, TRAIN_TYPE,
                               seed=random_seed, use_cache=use_cache)
    test_set = SiameseDataset(dataset_path, input_transformer, TEST_TYPE,
                              seed=random_seed, use_cache=use_cache)
    val_set = SiameseDataset(dataset_path, input_transformer, VAL_TYPE,
                             seed=random_seed, use_cache=use_cache)

    evaluation_set = SiameseDataset(evaluation_df, input_transformer, -1)
    evaluation_loader = DataLoader(evaluation_set, batch_size=batch_size, shuffle=False)

    return (train_set, test_set, val_set), evaluation_loader
