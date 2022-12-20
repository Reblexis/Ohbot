from collections import namedtuple
import numpy as np
import mediapipe as mp
import cv2

from constants import *

# Offsets are ordered (x_min, x_max, y_min, y_max)
OFFSETS = (0.02, 0.02, 0.14, 0.02)


class FaceDetection:
    def __init__(self):
        self.pipeline = mp.solutions.face_detection.FaceDetection()

    @staticmethod
    def draw_visualization(visualization_image: np.ndarray, face_infos: list) -> np.ndarray:
        for face_info in face_infos:
            cv2.rectangle(visualization_image, (face_info.x_min, face_info.y_min), (face_info.x_max, face_info.y_max),
                          (0, 0, 255), 2)
        return visualization_image

    def predict(self, image: np.ndarray, visualized_predictions: np.ndarray) -> tuple:
        assert image.shape == visualized_predictions.shape
        predicted_faces = []
        results = self.pipeline.process(image)
        if results.detections:
            for _, detection in enumerate(results.detections):
                detected_face = detection.location_data.relative_bounding_box

                face_x_min = int(max(detected_face.xmin - OFFSETS[0], 0) * image.shape[1])
                face_x_max = int(min((detected_face.xmin+detected_face.width) + OFFSETS[1], 1) * image.shape[1])
                face_y_min = int(max(detected_face.ymin - OFFSETS[2], 0) * image.shape[0])
                face_y_max = int(min((detected_face.ymin + detected_face.height) + OFFSETS[3], 1) * image.shape[0])
                face_image = image[face_y_min:face_y_max, face_x_min:face_x_max]

                face_info = FACE_INFO(face_x_min, face_x_max, face_y_min, face_y_max, face_image, None)

                predicted_faces.append(face_info)

        visualized_predictions = self.draw_visualization(visualization_image=visualized_predictions,
                                                         face_infos=predicted_faces)
        return predicted_faces, visualized_predictions
