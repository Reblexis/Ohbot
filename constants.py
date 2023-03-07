from collections import namedtuple
from pathlib import Path

from DataManagment.file_system import ensure_dir, save_to_file, load_file

DEVICE = "cuda"

DATA_FOLDER = Path.home() / "Data" / "Ohbot"
assert DATA_FOLDER.exists()

OTHER_FOLDER = DATA_FOLDER / "Other"

MODELS_FOLDER = DATA_FOLDER / "Models"
ensure_dir(MODELS_FOLDER)

ADMIN_ID = "admin"
UNKNOWN_ID = "unknown"
FACE_INFO = namedtuple("FACE_INFO", ["x_min", "x_max", "y_min", "y_max", "image", "id"])
FACE_RECOGNITION_MODEL = MODELS_FOLDER / "FaceRecognitionModel_12_19_2022_16_42_51"

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
