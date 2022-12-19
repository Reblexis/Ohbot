import base64
import cv2
import eel

from Function.Vision.face_detection import FaceDetection
from Function.Vision.face_recognition import FaceRecognition

CAMERA_DIMS = (1920, 1080)
CAMERA_PORT = 1


class VisionController:
    def __init__(self):
        print("Initializing vision controller...")
        self.camera = cv2.VideoCapture(CAMERA_PORT)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_DIMS[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_DIMS[1])

        self.face_detection_pipeline = FaceDetection()
        self.face_recognition_pipeline = FaceRecognition()

        self.admin_face = cv2.imread("admin_face.jpg")
        print("Vision controller initialized!")

    def get_frame(self, face_detections: bool = False, face_recognition: bool = False) -> tuple:
        success, image = self.camera.read()

        detected_faces, visualized_prediction = self.face_detection_pipeline.predict(image)
        image = visualized_prediction
        for pos, face in detected_faces:
            admin_probability = self.face_recognition_pipeline.predict(self.admin_face, face)
            print("Admin probability: ", 1-admin_probability)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def gen(self):
        while True:
            frame = self.get_frame()
            yield frame

    def show_camera_feed(self):
        y = self.gen()
        for each in y:
            blob = base64.b64encode(each)
            blob = blob.decode("utf-8")
            eel.showCameraFeed(blob)()
