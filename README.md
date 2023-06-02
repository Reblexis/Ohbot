## Thoughtful Artificially intelligent and Responsive System (TARS)

The goal of this project is to develop a human-like agent using artificial intelligence. The agent will be able to communicate with the user via speech just like a normal human, solve problems and much more.
You can read more details about the vision for this project (here)[].

## Installation
1. Clone the repository.
2. Create your preferred virtual environment.
3. Go to the repository folder and run `pip install -r requirements.txt` to install all the required packages.
4. If you want to use the trained models you have to retrieve them using git lfs like this: `git lfs pull`.
5. You can now run the software by running [main.py](main.py).

## Training
If you would like to replicate the training of the models, you can download the datasets [here](https://drive.google.com/file/d/1nj4l2pW25RxiD6ey25Xw8ZXcX6VLS_xh/view?usp=sharing).
You can run the training of the models by running `Training/Module/Aspect/trainer.py`. For example, if you would like to train the Face Recognition model,
you would run the file [Training/Vision/FaceRecognition/trainer.py](Training/Vision/FaceRecognition/trainer.py).

## Documentation
If you'd like to contribute to the project or want to learn more details about the project,
you can find more detailed documentation in the [Documentation](Documentation) folder.

Note that there may be bugs or unresolved issues in the code. If you find any, please report them in the [Issues](https://github.com/Reblexis/TARS/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) section.
