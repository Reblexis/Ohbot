from constants import *
from helpful_functions import clear_folder_content, ensure_dir

import shutil

folder = EMOV_DATASET_FOLDER

ensure_dir(folder / "samples")

for root, dirs, files in os.walk(folder):
    for filename in files:
        file = Path(os.path.join(root, filename))
        if file.suffix == ".wav" and file.parent.parent.name != EMOV_FOLDER:
            shutil.copy(file, (folder / "samples") / (filename[:-4] + "_" + file.parent.parent.name + ".wav"))
