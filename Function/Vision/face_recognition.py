import numpy as np
import torch

from constants import *
from Training.Vision.FaceRecognition.trainer import load_model


class FaceRecognition:
    def __init__(self):
        self.model, self.input_extractor, self.specs = load_model(FACE_RECOGNITION_MODEL)

    def predict(self, image1: np.ndarray, image2: np.ndarray) -> float:
        # Images are currently (H, W, C) but need to be (C, H, W)
        # Gets two images and returns the probability that they are different person
        image1 = np.transpose(image1, (2, 0, 1))
        image2 = np.transpose(image2, (2, 0, 1))
        # Shape is (C, H, W)
        image1 = torch.from_numpy(image1).float()
        image2 = torch.from_numpy(image2).float()

        image1 = self.input_extractor(image1)
        image2 = self.input_extractor(image2)

        image1 = image1.unsqueeze(0)
        image2 = image2.unsqueeze(0)
        # Shape is (1, C, H, W)

        image1 = image1.to(DEVICE)
        image2 = image2.to(DEVICE)

        x = torch.cat((image1, image2), dim=0)
        print(x.shape)
        # duplicate along batch dimension
        print(x.shape)
        output = self.predict_batch(x.unsqueeze(0))
        return output[0][0].item()

    def predict_batch(self, images: torch.tensor) -> np.ndarray:
        print(images.shape)
        return self.model(images)
