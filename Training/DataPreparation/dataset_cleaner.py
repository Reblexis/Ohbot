import uuid
import re
import shutil
import pandas as pd

from Training.training_constants import *
from DataManagment.file_system import ensure_dir, clear_folder_content, save_to_file, load_file


def clean_dataset(dataset_to_clean: Path, process_function):
    print("Cleaning dataset:", dataset_to_clean)

    samples_info = []

    cleaned_dataset_path = CLEANED_DATASETS_FOLDER / dataset_to_clean.name
    ensure_dir(cleaned_dataset_path)
    clear_folder_content(cleaned_dataset_path)
    ensure_dir(cleaned_dataset_path / SAMPLES_FOLDER)
    ensure_dir(cleaned_dataset_path / DATASET_INFO_FOLDER)

    for file in dataset_to_clean.iterdir():
        if file.name.endswith(".wav"):
            sample_rate, audio_data = load_file(file)
            audio_data = resample_audio(audio_data, sample_rate, TRAINING_RATE)

            data = process_function(file.name)  # File name at index 0

            data["path"] = cleaned_dataset_path / SAMPLES_FOLDER / f"{uuid.uuid4().hex}.wav"

            samples_info.append(data)
            save_to_file(audio_data, data["path"], {"type": "audio", "sample_rate": TRAINING_RATE})

    samples_info_df = pd.DataFrame(samples_info)
    dataset_info["emotions"] = list(samples_info_df["emotion"].unique())
    save_to_file(samples_info_df, cleaned_dataset_path / DATASET_SAMPLES_DF)
    save_to_file(dataset_info, cleaned_dataset_path / DATASET_INFO_FILE)

    debug_message(("dataset cleaning", dataset_to_clean), 1, 1)


def process_file_dataverse(file_name: str) -> dict:
    file_info = re.split('_|\.', file_name)

    speaker_id = file_info[0]
    emotion = DATAVERSE_EMOTION_MAPPING[file_info[2]]

    return {"speaker_id": speaker_id, "emotion": emotion}


def clean():
    clean_dataset(JL_DATASET_FOLDER, process_file_JL)
    clean_dataset(DATAVERSE_DATASET_FOLDER, process_file_dataverse)
    clean_dataset(CREMA_DATASET_FOLDER, process_file_crema)
    clean_dataset(RAVDESS_DATASET_FOLDER, process_file_RAVDESS)
    clean_dataset(ASVP_DATASET_FOLDER, process_file_ASVP)
    clean_dataset(EMOV_DATASET_FOLDER, process_file_emo_v)


if __name__ == "__main__":
    clean()
