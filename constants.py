from pathlib import Path

from DataManagment.file_system import ensure_dir, save_to_file, load_file

DEVICE = "cuda"

DATA_FOLDER = Path("C:/Data/Personal/Ohbot/")
assert DATA_FOLDER.exists()

MODELS_FOLDER = DATA_FOLDER / "Models"
ensure_dir(MODELS_FOLDER)

FACE_RECOGNITION_MODEL = MODELS_FOLDER / "FaceRecognitionModel_12_19_2022_16_42_51"

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
