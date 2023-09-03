from Training.training_constants import *
from DataManagement.file_system import clear_folder_content, ensure_dir, clear_folder_content

import os
import shutil

input("Are you sure you want to move all files from subfolders to parent folder?")

folder = RAW_DATASETS.DIGI_FACE

ensure_dir(folder / "samples")
clear_folder_content(folder / "samples")
suffix = ".png"

contents = list(os.walk(folder))
for root, dirs, files in contents:
    for filename in files:
        file = Path(os.path.join(root, filename))
        if file.suffix == suffix:
            shutil.copy(file, (folder / "samples") / (filename[:-4] + "_" + file.parent.name + suffix))

