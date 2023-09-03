# Developer documentation

This documentation explains how to contribute to the project and how to use the software in more detail. If you haven't read the [README.md](../README.md) file or the [user documentation](user_documentation.md), please do so first.

## Project structure
The project is split into 5 main parts (it uses camel case for folders and snake case for files):
- `App` - the web application, that allows you to interact with the robot
- `Documentation` - the developer and the user documentation of the project
- `DataManagement` - helper scripts for data management
- `Function` - different modules controlling the robot
- `Training` - scripts for training AI models used in the project

### Web app
The app currently gives you access to a console, via which you can interact with the robot [command_manager.py](../Function/Core/command_manager.py).
It uses the flask library at the moment.

### DataManagement
This folder contains scripts for managing folder creation and file management in general. Also contains some helper functions
used throughout the project.

### Function
This folder contains the main modules of the robot. Each module is responsible for something different:
- `Core` - the core module, which joins all modules together and allows for the interaction between them
- `Vision` - the vision module, it extracts data from the camera and processes it
- `Speech` - the speech module, currently it allows mainly for text to speech purposes
- `Hearing` - the hearing module, it analyzes microphone input and currently serves mainly for real time speech recognition

### Training
This folder contains scripts for training AI models used in the project.
At the moment it contains the training scripts used to train the face recognition model.

