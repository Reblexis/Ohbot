from Training.Vision.FaceRecognition.Models.model_manager import Model

import torch
import torch.nn as nn
from facenet_pytorch import InceptionResnetV1


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding, dropout=0.1):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        self.bn = nn.BatchNorm2d(out_channels)
        self.dropout = nn.Dropout2d(dropout) if dropout > 0 else None
        self.relu = nn.LeakyReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        if self.dropout is not None:
            x = self.dropout(x)
        return x


class MaxPoolBlock(nn.Module):
    def __init__(self, kernel_size=(3, 3), stride: tuple = (2, 2), padding=(1, 1)):
        super().__init__()
        self.pool = nn.MaxPool2d(kernel_size, stride, padding)

    def forward(self, x):
        return self.pool(x)


class LinearBlock(nn.Module):
    def __init__(self, in_features, out_features, dropout=0.2):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.batch_norm = nn.BatchNorm1d(out_features)
        self.relu = nn.LeakyReLU()
        self.dropout = nn.Dropout(dropout) if dropout > 0 else None

    def forward(self, x):
        x = self.linear(x)
        x = self.batch_norm(x)
        x = self.relu(x)
        if self.dropout is not None:
            x = self.dropout(x)
        return x


class L1Distance(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x1, x2):
        return torch.abs(x1 - x2)


class InceptionResnetNetwork(Model):
    """
    Pretrained inception resnet model.
    Receives two images and outputs a similarity score between 0 and 1.
    """

    def __init__(self, loss_function, optimizer, train_test_sets: tuple,
                 hyper_params: dict):
        super().__init__(loss_function, optimizer, train_test_sets, hyper_params)

    def init_model(self):
        # input_shape = (3, 128, 128)
        in_channels = 3
        model = InceptionResnetV1(pretrained='vggface2')
        # freeze the model
        for param in model.parameters():
            param.requires_grad = False
        self.embedding = model
        self.l1_dist = L1Distance()
        self.embedding_linear = nn.Sequential(
            LinearBlock(512, 256),
            LinearBlock(256, 128),
        )
        self.classifier_layer = nn.Sequential(
            LinearBlock(128, 64),
            LinearBlock(64, 32),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        # X shape (batch_size, 2, 3, 128, 128) (2 because of the 2 images to be compared)
        x1 = self.embedding(x[:, 0, :, :, :])
        x2 = self.embedding(x[:, 1, :, :, :])
        x1 = self.embedding_linear(x1)
        x2 = self.embedding_linear(x2)
        x = self.l1_dist(x1, x2)
        x = self.classifier_layer(x)
        return x


def find_out_needed_shape():
    pass
    """
    model = BaselineModel(nn.CrossEntropyLoss(), torch.optim.Adam,
                          get_train_test_sets(CLEANED_DATASETS_FOLDER / DATAVERSE_FOLDER,
                                              MFCCExtractor(), IndexExtractor()), (513, 7))
    test_tensor = torch.randn(1, 1, 513, 257)
    out = model(test_tensor)"""
