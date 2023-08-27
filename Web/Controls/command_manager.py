import re

from Function.Core.core_controller import CoreController

# TODO: Change this into one dictionary indexed by the command names
# TODO: Implement better delimiter than space
DEFAULT_RESET_ARGS = {"aspect": "all"}
DEFAULT_ROTATE_ARGS = {"obj": "head", "horizontal": 0.5, "vertical": 0.5}  # Slight rotation to the right and up
DEFAULT_SET_ARGS = {"obj": "camera", "state": "on"}
DEFAULT_SAY_ARGS = {"text": "The text that the agent will say"}
DEFAULT_HELP_ARGS = {"command": "command_you_want_to_know_more_about"}


class Parameter:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class ContinuousParameter(Parameter):

    def __init__(self, name: str, description: str, minimum: float, maximum: float, default: float):
        super().__init__(name, description)

        self.min = minimum
        self.max = maximum
        self.default = default
        assert self.min <= self.default <= self.max

    def __str__(self):
        return (
            f"A continuous floating number parameter ranging from {self.min} to {self.max} with default value {self.default}. "
            f"Description: {self.description}")


class DiscreteParameter(Parameter):
    def __init__(self, name: str, description: str, options: list, default: str):
        super().__init__(name, description)

        self.options = options
        self.default = default
        assert self.default in self.options

    def __str__(self):
        return (f"A discrete parameter with options {self.options} and default value {self.default}. "
                f"Description: {self.description}")


class TextParameter(Parameter):
    """
    A parameter that accepts text as input.
    """

    def __init__(self, name: str, description: str, default: str):
        super().__init__(name, description)

        self.default = default

    def __str__(self):
        return (f"A text parameter with default value {self.default}. "
                f"Description: {self.description}")


class Command:
    def __init__(self, name: str, description: str, parameters: list):
        self.name = name
        self.description = description
        self.parameters = parameters

    def __str__(self):
        answer: str = f"Command: {self.name}\nDescription: {self.description}\nParameters:\n"
        for parameter in self.parameters:
            answer += f"{parameter}\n"
        answer += f"Example usage: {self.name} "
        for parameter in self.parameters:
            answer += f"{parameter.name}={parameter.default} "
        return answer


class ResetCommand(Command):
    def __init__(self):
        super().__init__("reset", "Resets different aspects or functionalities of the robot.",
                         [DiscreteParameter("aspect", "The aspect to reset.", ["all", "motors", "camera"],
                                            DEFAULT_RESET_ARGS["aspect"])])


class RotateCommand(Command):
    def __init__(self):
        super().__init__("rotate", "Rotates the head of the robot.",
                         [ContinuousParameter("horizontal", "Horizontal angle to rotate to. Ranges from -1 (left)"
                                                            " to 1 (right).", -1, 1, DEFAULT_ROTATE_ARGS["horizontal"]),
                          ContinuousParameter("vertical", "Vertical angle to rotate to. Ranges from -1 (down)"
                                                          " to 1 (up).", -1, 1, DEFAULT_ROTATE_ARGS["vertical"])])


class SetCommand(Command):
    def __init__(self):
        super().__init__("set", "Changes state of a certain aspect of the robot. Toggles functionalities on or off.",
                         [DiscreteParameter("obj", "The object to change the state of.", ["camera", "microphone"],
                                            DEFAULT_SET_ARGS["obj"]),
                          DiscreteParameter("state", "The state to change to.", ["on", "off"],
                                            DEFAULT_SET_ARGS["state"])])


class SayCommand(Command):
    def __init__(self):
        super().__init__("say", "Makes the robot say something.", [TextParameter("text", "The text to say.",
                                                                                 DEFAULT_SAY_ARGS["text"])])


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help", "Gives information about a certain command and explains how to use it.",
                         [TextParameter("command", "The command to get help about.", DEFAULT_HELP_ARGS["command"])])


class CommandManager:

    def __init__(self, core_controller: CoreController):
        self.commands = {"reset": (self.reset, ResetCommand), "rotate": (self.rotate, RotateCommand),
                         "set": (self.set, SetCommand), "say": (self.say, SayCommand),
                         "help": (self.help, HelpCommand)}
        self.core_controller = core_controller

    @staticmethod
    def get_arg(args, key, default):
        if key in args:
            return args[key]
        return default

    @staticmethod
    def update_args(args: dict, default_args: dict):
        for key, value in default_args.items():
            if key not in args:
                args[key] = value
        return args

    def reset(self, args: dict):
        pass

    def rotate(self, args: dict):
        cur_args = self.update_args(args, DEFAULT_ROTATE_ARGS)
        self.core_controller.physical_controller.rotate_head_to(horizontal=float(cur_args["horizontal"]),
                                                                vertical=float(cur_args["vertical"]))

    def set(self, args: dict):
        cur_args = self.update_args(args, DEFAULT_SET_ARGS)
        if cur_args["obj"] == "camera":
            if cur_args["state"] == "on" and not self.core_controller.vision_controller.show_camera:
                self.core_controller.vision_controller.enable()
            elif cur_args["state"] == "off" and self.core_controller.vision_controller.show_camera:
                self.core_controller.vision_controller.disable()
        elif cur_args["obj"] == "microphone":
            if cur_args["state"] == "on" and not self.core_controller.hearing_controller.listening:
                self.core_controller.hearing_controller.enable()
            elif cur_args["state"] == "off" and self.core_controller.hearing_controller.listening:
                self.core_controller.hearing_controller.disable()

    def say(self, args: dict):
        text = self.get_arg(args, "text", "Hello!")
        self.core_controller.speech_controller.process(text)

    def help(self, args: dict) -> str:
        command = self.get_arg(args, "command", "undefined_command")
        if command in self.commands:
            return str(self.commands[command][1]())
        return "No such command found."

    def execute_command(self, command: str) -> bool:
        # command form should be "command_name arg1_name=arg1_value arg2_name=arg2_value..."
        command_name, *args = command.split(" ")
        try:
            args = {arg.split("=")[0]: arg.split("=")[1] for arg in args}
        except:
            return False
        if command_name in self.commands:
            print(f"Executing command {command_name} with args {args}")
            self.commands[command_name](args)
            return True
        else:
            return False
