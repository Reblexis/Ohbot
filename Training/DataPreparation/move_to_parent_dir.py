from Training.training_constants import *
from DataManagement.file_system import clear_folder_content, ensure_dir, clear_folder_content

import os
import shutil

folder = RAW_DATASETS.DIGI_FACE / "samples"

ensure_dir(folder)
suffix = ".png"

contents = list(os.walk(folder))
for root, dirs, files in contents:
    for filename in files:
        file = Path(os.path.join(root, filename))
        if file.suffix == suffix:
            # Move to parent directory
            shutil.move(file, file.parent.parent / filename)
