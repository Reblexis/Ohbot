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
    NO_CAMERA_PLACEHOLDER = OTHER_FOLDER / "no_camera.jpg"

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

    def get_frame(self, face_detections: bool = True, face_recognition: bool = False) -> np.ndarray:
        if not self.show_camera:
            return cv2.imread(str(self.NO_CAMERA_PLACEHOLDER))

        success, image = self.camera.read()
        assert success, "Failed to get frame from camera!"
        visualized_predictions = image.copy()
        faces = self.face_detection_pipeline.predict(image, visualized_predictions)
        if face_recognition:
            faces = self.face_recognition_pipeline.predict_faces(faces, visualized_predictions)

        visualized_predictions = cv2.resize(visualized_predictions, self.SHOWN_CAMERA_DIMS)

        return visualized_predictions

    @staticmethod
    def numpy_to_bytes(array_to_encode: np.ndarray):
        _, buffer = cv2.imencode('.jpg', array_to_encode)
        return buffer.tobytes()

    def gen_frames(self):
        while True:
            numpy_buffer = self.get_frame()
            buffer = self.numpy_to_bytes(numpy_buffer)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n')

    def step(self):
        last_frame = self.get_frame()

    def enable(self):
        self.show_camera = True

    def disable(self):
        self.show_camera = False

    def step(self):
        pass
