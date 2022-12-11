from Training.Vision.FaceRecognition.face_recognition_constants import *
from Training.training_constants import *
from DataManagment.file_system import load_file, save_to_file

import pandas as pd
import random

pd.options.mode.chained_assignment = None  # default='warn'

datasets = [DATASETS.DIGI_FACE]
people_amount = [100]
random_identifier = str(random.randint(0, 100000000))

evaluation_samples = None

for i, dataset in enumerate(datasets):
    dataset_path = CLEANED_DATASETS_FOLDER / dataset
    dataset_samples = load_file(dataset_path / DATASET_SAMPLES_DF)
    people = list(dataset_samples["person_id"].unique())
    random.shuffle(people)
    to_use = people[0: people_amount[i]]
    next_samples = dataset_samples[dataset_samples["person_id"].isin(to_use)]
    # dataset_name = ([str(datasets[i])] * len(next_samples))
    # next_samples.loc[:, 'dataset'] = dataset_name

    if evaluation_samples is None:
        evaluation_samples = next_samples
    else:
        evaluation_samples = pd.concat(evaluation_samples, next_samples)

save_to_file(evaluation_samples, EVALUATION_FOLDER / f"samples_{random_identifier}.csv")
