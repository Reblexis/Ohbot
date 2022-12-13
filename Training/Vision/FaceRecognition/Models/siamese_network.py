from Training.Vision.FaceRecognition.Models.model_manager import Model

import torch
import torch.nn as nn


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
        self.relu = nn.LeakyReLU()
        self.dropout = nn.Dropout(dropout) if dropout > 0 else None

    def forward(self, x):
        x = self.linear(x)
        x = self.relu(x)
        if self.dropout is not None:
            x = self.dropout(x)
        return x


class L1Distance(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x1, x2):
        return torch.abs(x1 - x2)


class SiameseNetwork(Model):
    """
    Convolutional model for face recognition.
    Receives two images and outputs a similarity score between 0 and 1.
    """

    def __init__(self, loss_function, optimizer, train_test_sets: tuple,
                 hyper_params: dict):
        super().__init__(loss_function, optimizer, train_test_sets, hyper_params)

    def init_model(self):
        # input_shape = (1, 64, 64) if grayscale else (3, 64, 64)
        in_channels = 1 if self.hyperparams["grayscale"] else 3
        self.cnn = nn.Sequential(
            ConvBlock(in_channels=in_channels, out_channels=32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
            ConvBlock(in_channels=32, out_channels=32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
            MaxPoolBlock(),
            ConvBlock(in_channels=32, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
            ConvBlock(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
            MaxPoolBlock(),
            ConvBlock(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
            ConvBlock(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
            MaxPoolBlock(),
            ConvBlock(in_channels=64, out_channels=128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
            ConvBlock(in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
        )
        self.flatten_layer = nn.Flatten()
        self.fc = nn.Sequential(
            LinearBlock(in_features=8192, out_features=512),
            LinearBlock(in_features=512, out_features=256),
            nn.Linear(in_features=256, out_features=self.hyperparams['features_dim']),
            nn.Sigmoid(),
        )
        self.embedding = nn.Sequential(self.cnn, self.flatten_layer, self.fc)
        print(self.embedding)
        self.l1_dist = L1Distance()
        self.classifier_layer = nn.Sequential(nn.Linear(self.hyperparams['features_dim'], 1), nn.Sigmoid())

    def forward(self, x):
        # X shape (batch_size, 2, 1, 128, 128) (2 because of the 2 images to be compared)
        x1 = self.embedding(x[:, 0, :, :, :])
        x2 = self.embedding(x[:, 1, :, :, :])
        l1_distance = self.l1_dist(x1, x2)
        output = self.classifier_layer(l1_distance)
        return output


def find_out_needed_shape():
    pass
    """
    model = BaselineModel(nn.CrossEntropyLoss(), torch.optim.Adam,
                          get_train_test_sets(CLEANED_DATASETS_FOLDER / DATAVERSE_FOLDER,
                                              MFCCExtractor(), IndexExtractor()), (513, 7))
    test_tensor = torch.randn(1, 1, 513, 257)
    out = model(test_tensor)"""
