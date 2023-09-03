# User documentation

This documentation explains how to use the software in more detail. If you haven't read the [README.md](../README.md) file, please do so first.

## Initial setup
After running the `main.py` file, you may have to enter your OPENAI API key into console as well as the audio input device you intend to use.
It's not possible to customize your camera at the moment without accessing the code. If you want to change it, you can go into [vision_controller.py](../Function/Vision/vision_controller.py) and change the `CAMERA_PORT` variable.
After that, you should have the web interface available at the address given to you in the console / terminal.
If you don't have the physical robot connected to your computer, just click on the `Connect` button and 
later on the `Connect anyway (experimental)` button. You should still have access to all the functionalities but the `rotate` command won't work.

## Console
After running the app via `App/main.py` and connecting to the agent, you will be presented with a console. 
The console allows you to enter individual commands with which you can experiment with the different functions of the robot. 
Each command may have its own parameters. Use can use the command `help` to get a list of all available commands. 
If you type `help --command=<command>` you will get a more detailed description of the command and its parameters.

## Interaction with the robot using speech
If you want to talk to the robot you have to first enable the microphone via the command `toggle --obj=microphone` in the console.
Afterward whenever you use the wake-word 'assistant' the robot will start listening to you. You can then say something and the robot will respond to it.
You can follow the agent's actions in the console. If you want to disable the microphone you can use the command `toggle --obj=microphone --state=off`.
You can customize the wake-words in the [speech_recognition_.py](../Function/Hearing/speech_recognition_.py) file.
