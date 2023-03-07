import base64
import cv2
import matplotlib.image as mpimg
import eel

from Function.Vision.face_detection import FaceDetection
from Function.Vision.face_recognition import FaceRecognition


class VisionController:
    CAMERA_DIMS = (1920, 1080)
    SHOWN_CAMERA_DIMS = (960, 540)
    CAMERA_PORT = -1

    def __init__(self):
        print("Initializing vision controller...")
        self.camera = cv2.VideoCapture(self.CAMERA_PORT)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_DIMS[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_DIMS[1])

        self.face_detection_pipeline = FaceDetection()
        self.face_recognition_pipeline = FaceRecognition()

        self.face_detection_pipeline.visualize = True
        self.face_recognition_pipeline.visualize = True

        self.show_camera = False
        print("Vision controller initialized!")

    def get_frame(self, face_detections: bool = False, face_recognition: bool = False) -> tuple:
        success, image = self.camera.read()
        visualized_predictions = image.copy()
        faces = self.face_detection_pipeline.predict(image, visualized_predictions)
        faces = self.face_recognition_pipeline.predict_faces(faces, visualized_predictions)

        visualized_predictions = cv2.resize(visualized_predictions, SHOWN_CAMERA_DIMS)

        ret, jpeg = cv2.imencode('.jpg', visualized_predictions)
        return jpeg.tobytes()

    def gen(self):
        while self.show_camera:
            frame = self.get_frame()
            yield frame

    def show_camera_feed(self):
        self.show_camera = True
        y = self.gen()
        for each in y:
            blob = base64.b64encode(each)
            blob = blob.decode("utf-8")
            eel.showCameraFeed(blob)()
