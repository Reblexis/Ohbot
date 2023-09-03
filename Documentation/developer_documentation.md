# Developer documentation

This documentation explains the code structure of the project and how to use the software in more detail. If you haven't read the [README.md](../README.md) file or the [user documentation](user_documentation.md), please do so first.

## Project structure
The project is split into 5 main parts (it uses camel case for folders and snake case for files):
- `App` - the web application, that allows you to interact with the robot
- `Documentation` - the developer and the user documentation of the project
- `DataManagement` - helper scripts for data management
- `Function` - different modules controlling the robot
- `Training` - scripts for training AI models used in the project
- `Data` - data used in the project - images, audio files, models, etc.

### Web app
The app currently gives you access to a console, via which you can interact with the robot [command_manager.py](../Function/Core/command_manager.py).
It uses the flask library at the moment.
It's composed of the following scripts:
- [web.py](../Web/web.py) - contains the web class and flask communication between the server and the client
- [templates/menu.html](../Web/templates/menu.html) - initial web page allowing the user to connect to the agent
- [templates/main.html](../Web/templates/main.html) - the main web page, which contains the console and the video feed

### DataManagement
This folder contains scripts for managing folder creation and file management in general. Also contains some helper functions
used throughout the project.
It's composed of the following scripts:
- [file_system.py](../DataManagement/file_system.py) - contains helper functions related to file storage
- [image_system.py](../DataManagement/image_system.py) - contains helper functions related to image processing


### Function
This folder contains the main modules of the robot. Each module is responsible for something different:

#### Core
The core module, which joins all modules together and allows for the interaction between them.
It's composed of the following scripts:
- [command_manager.py](../Function/Core/command_manager.py) - the command manager, which allows for the interaction with the agent and its functionalities 
- [core_controller.py](../Function/Core/core_controller.py) - the core controller, which joins all modules together and allows for the interaction between them

#### Vision
The vision module, it extracts data from the camera and processes it.
It's composed of the following scripts:
- [vision_controller.py](../Function/Vision/vision_controller.py) - the vision controller, which joins all vision modules together and allows for the interaction between them
- [face_recognition.py](../Function/Vision/face_recognition.py) - the face recognition module, which allows for the recognition of faces via siamese neural network
- [face_detection.py](../Function/Vision/face_detection.py) - the face detection module, which allows for the detection of faces 

#### Speech
The speech module, currently it allows mainly for text to speech purposes.
It's composed of the following scripts:
- [speech_controller.py](../Function/Speech/speech_controller.py) - the speech controller, which joins all speech modules together and allows for the interaction between them
- [talking.py](../Function/Speech/talking.py) - the talking module, which allows for the text to speech functionality

#### Hearing
The hearing module, it analyzes microphone input and currently serves mainly for real time speech recognition.
It's composed of the following scripts:
- [hearing_controller.py](../Function/Hearing/hearing_controller.py) - the hearing controller, which joins all hearing modules together and allows for the interaction between them
- [speech_recognition_.py](../Function/Hearing/speech_recognition_.py) - the speech recognition module, which allows for the speech recognition functionality

#### Physical
The physical module, it allows for the interaction with the physical robot.
It's composed of the following scripts:
- [physical_controller.py](../Function/Physical/physical_controller.py) - the physical controller, it communicates with the physical robot via serial communication
- [helpful_functions.py](../Function/Physical/helpful_functions.py) - contains helper functions for the physical controller


### Training
This folder contains scripts for training AI models used in the project.
At the moment it contains the training scripts used to train the face recognition model.
It will be restructured soon, so I won't go into much detail into the current structure.
The current structure looks something like this:
- `DataPipeline` - creates train / val / test datasets which serve for loading the data into the models
- `DataPreparation` - prepares the data for training, e.g. renames files, creates dataset csv files, etc.
- `Evaluation` - contains scripts for evaluating the models
- `Extractors` - contains scripts for extracting features from the data can be the input data into the models but also the output data from the models
- `Vision` - contains scripts for training vision models
- `Vision/FaceRecognition` - contains scripts for training the face recognition model
- `Vision/FaceRecognition/Models` - different architectures and model_manager which contains abstract class for all models (uses pytorch lightning)
- `Vision/FaceRecognition/dataset.py` - contains the siamese dataset class, which is responsible for feeding the data into the siamese network
- `Vision/FaceRecognition/trainer.py` - contains the trainer class, which is the main class which launches the training and analyzes its performance using wandb library
- `Vision/FaceRecognition/constants.py` - contains constants used throughout the training process and dataset preparation
- `Vision/FaceRecognition/hyperparameters.py` - contains hyperparameters used throughout the training process
