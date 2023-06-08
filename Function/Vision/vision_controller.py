import os

import cv2
from constants import *
import numpy as np

from Function.Vision.face_detection import FaceDetection
from Function.Vision.face_recognition import FaceRecognition


class VisionController:
    CAMERA_DIMS = (1920, 1080)
    SHOWN_CAMERA_DIMS = (960, 540)
    CAMERA_PORT = 0

    # Two different files so that another process doesn't read the file while it's being rewritten
    LAST_FRAME_WRITE_PATH = OTHER_FOLDER / "last_frame_write.jpg"
    LAST_FRAME_READ_PATH = OTHER_FOLDER / "last_frame_read.jpg"

    def __init__(self):
        print("Initializing vision controller...")
        self.camera = cv2.VideoCapture(self.CAMERA_PORT)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_DIMS[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_DIMS[1])
        success, image = self.camera.read()
        assert success, f"Camera isn't working or isn't available on port {self.CAMERA_PORT}!"

        self.face_detection_pipeline = FaceDetection()
        self.face_recognition_pipeline = FaceRecognition()

        self.face_detection_pipeline.visualize = True
        self.face_recognition_pipeline.visualize = True

        self.show_camera = False
        print("Vision controller initialized!")

    def get_frame(self, face_detections: bool = False, face_recognition: bool = False) -> np.ndarray:
        success, image = self.camera.read()
        assert success, "Failed to get frame from camera!"
        visualized_predictions = image.copy()
        faces = self.face_detection_pipeline.predict(image, visualized_predictions)
        if face_recognition:
            faces = self.face_recognition_pipeline.predict_faces(faces, visualized_predictions)

        visualized_predictions = cv2.resize(visualized_predictions, self.SHOWN_CAMERA_DIMS)

        return visualized_predictions

    def gen_frames(self):
        # Currently not supported
        return

    def step(self):
        last_frame = self.get_frame()

    def enable(self):
        self.show_camera = True

    def disable(self):
        self.show_camera = False
