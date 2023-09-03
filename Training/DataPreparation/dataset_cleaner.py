import uuid
import re
import shutil
import pandas as pd

from Training.training_constants import *
from DataManagement.file_system import ensure_dir, clear_folder_content, save_to_file, load_file
from DataManagement.image_system import convert_to_gray

suffix = ".png"


def clean_dataset(dataset_to_clean: Path, process_function):
    print("Cleaning dataset:", dataset_to_clean)

    samples_info = []

    cleaned_dataset_path = CLEANED_DATASETS_FOLDER / dataset_to_clean.name
    ensure_dir(cleaned_dataset_path)
    clear_folder_content(cleaned_dataset_path)
    ensure_dir(cleaned_dataset_path / SAMPLES_FOLDER)

    for file in dataset_to_clean.iterdir():
        if file.name.endswith(suffix):
            content = load_file(file)

            # content = convert_to_gray(content)

            data = process_function(file.name)  # File name at index 0

            data["path"] = cleaned_dataset_path / SAMPLES_FOLDER / (f"{uuid.uuid4().hex}" + suffix)

            samples_info.append(data)
            save_to_file(content, data["path"], additional_info={"type": "image"})

    samples_info_df = pd.DataFrame(samples_info)
    save_to_file(samples_info_df, cleaned_dataset_path / DATASET_SAMPLES_DF)

    print("Dataset cleaned: ", dataset_to_clean)


def process_file_difi_face(file_name: str) -> dict:
    file_info = re.split('_|\.', file_name)

    person_id = file_info[1]

    return {"person_id": person_id}


def clean():
    clean_dataset(RAW_DATASETS.DIGI_FACE, process_file_difi_face)


if __name__ == "__main__":
    clean()
