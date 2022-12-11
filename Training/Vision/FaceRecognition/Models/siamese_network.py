from Training.Vision.FaceRecognition.Models.model_manager import Model

import torch
import torch.nn as nn


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.LeakyReLU()

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class MaxPoolBlock(nn.Module):
    def __init__(self, kernel_size=(3, 3), stride: tuple = (2, 2), padding=(1, 1)):
        super().__init__()
        self.pool = nn.MaxPool2d(kernel_size, stride, padding)

    def forward(self, x):
        return self.pool(x)


class LinearBlock(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.relu = nn.LeakyReLU()

    def forward(self, x):
        return self.relu(self.linear(x))


class SiameseNetwork(Model):
    """
    Convolutional model for face recognition.
    Receives two images and outputs a similarity score between 0 and 1.
    """

    def __init__(self, loss_function, optimizer, train_test_sets: tuple,
                 input_output_shape: tuple, hyper_params: dict):
        super().__init__(loss_function, optimizer, train_test_sets, input_output_shape, hyper_params)

    def init_model(self):
        # input_shape = (1, 128, 128)
        self.cnn = nn.Sequential(
            ConvBlock(in_channels=1, out_channels=32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)),
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
            LinearBlock(in_features=128 * 16 * 16, out_features=128),
            LinearBlock(in_features=128, out_features=128),
            nn.Linear(in_features=128, out_features=16)
        )
        self.fc2 = nn.Sequential(
            LinearBlock(32, 32),
            LinearBlock(32, 32),
            nn.Linear(32, 1)
        )
        self.all_layers = nn.Sequential(self.cnn, self.flatten_layer, self.fc)

    def forward(self, x):
        # X shape (batch_size, 2, 128, 128) (2 because of the 2 images to be compared)
        x1 = self.all_layers(x[:, 0, :, :].unsqueeze(1))
        x2 = self.all_layers(x[:, 1, :, :].unsqueeze(1))
        concatenated = torch.cat((x1, x2), dim=1)
        y = self.fc2(concatenated)
        return y


def find_out_needed_shape():
    pass
    """
    model = BaselineModel(nn.CrossEntropyLoss(), torch.optim.Adam,
                          get_train_test_sets(CLEANED_DATASETS_FOLDER / DATAVERSE_FOLDER,
                                              MFCCExtractor(), IndexExtractor()), (513, 7))
    test_tensor = torch.randn(1, 1, 513, 257)
    out = model(test_tensor)"""
