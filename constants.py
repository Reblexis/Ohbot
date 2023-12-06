from collections import namedtuple
from pathlib import Path

DEVICE = "cpu"

DATA_FOLDER = Path(__file__).parent / "Data"

OTHER_FOLDER = DATA_FOLDER / "Other"
OTHER_FOLDER.mkdir(parents=True, exist_ok=True)

MODELS_FOLDER = DATA_FOLDER / "Models"
MODELS_FOLDER.mkdir(parents=True, exist_ok=True)

ADMIN_ID = "admin"
UNKNOWN_ID = "unknown"
FACE_INFO = namedtuple("FACE_INFO", ["x_min", "x_max", "y_min", "y_max", "image", "id"])
FACE_RECOGNITION_MODEL = MODELS_FOLDER / "FaceRecognitionModel_12_19_2022_16_42_51"

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
