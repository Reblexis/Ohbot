import numpy as np
import torch
import cv2
import matplotlib.image as mpimg

from constants import *
from Training.Vision.FaceRecognition.trainer import load_model

ADMIN_FACE_PATH = OTHER_FOLDER / "admin_face.jpg"


class FaceRecognition:
    """
    Predicts the probability that two images are different people. Works only on RGB images.
    """
    def __init__(self):
        self.model, self.input_extractor, self.specs = load_model(FACE_RECOGNITION_MODEL)
        self.admin_face = np.transpose(mpimg.imread(ADMIN_FACE_PATH), (2, 0, 1))
        self.model.eval()

    @staticmethod
    def draw_visualization(visualization_image: np.ndarray, face_infos: list) -> np.ndarray:
        for face_info in face_infos:
            cv2.putText(visualization_image, str(face_info.id), (face_info.x_min, face_info.y_min),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return visualization_image

    def predict_faces(self, faces: list, visualized_predictions: np.ndarray) -> tuple:
        faces_infos = []
        for i in range(len(faces)):
            face_info = faces[i]
            rgb_face = np.transpose(cv2.cvtColor(face_info.image, cv2.COLOR_BGR2RGB), (2, 0, 1))
            admin_probability = 1 - self.predict_pair(self.admin_face, rgb_face)
            predicted_id = ADMIN_ID if admin_probability > 0.75 else UNKNOWN_ID
            new_face_info = FACE_INFO(face_info.x_min, face_info.x_max, face_info.y_min, face_info.y_max,
                                      face_info.image, predicted_id)
            faces_infos.append(new_face_info)

        visualized_predictions = self.draw_visualization(visualization_image=visualized_predictions,
                                                         face_infos=faces_infos)
        return faces_infos, visualized_predictions

    def predict_pair(self, image1: np.ndarray, image2: np.ndarray) -> float:
        """
        Assumes received images are RGB. And in format (channels, height, width)
        """
        image1 = torch.from_numpy(image1).float()
        image2 = torch.from_numpy(image2).float()

        image1 = self.input_extractor(image1)
        image2 = self.input_extractor(image2)
        image1 = image1 / 255
        image2 = image2 / 255

        image1 = image1.unsqueeze(0)
        image2 = image2.unsqueeze(0)

        image1 = image1.to(DEVICE)
        image2 = image2.to(DEVICE)

        x = torch.cat((image1, image2), dim=0)
        output = self.model(x.unsqueeze(0))
        return output[0][0].item()

    def predict_batch(self, images: torch.tensor) -> np.ndarray:
        print(images.shape)
        return self.model(images)
