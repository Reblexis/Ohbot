import re

from Function.Core.core_controller import CoreController

DEFAULT_ROTATE_ARGS = {"obj": "head", "horizontal": 0.5, "vertical": 0.5}  # Slight rotation to the right and up
DEFAULT_SET_ARGS = {"obj": "camera", "state": "on"}


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


class DiscreteParameter(Parameter):
    def __init__(self, name: str, description: str, options: list, default: str):
        super().__init__(name, description)

        self.options = options
        self.default = default
        assert self.default in self.options


class Command:
    def __init__(self, name: str, description: str, parameters: list):
        self.name = name
        self.description = description
        self.parameters = parameters


class ResetCommand(Command):
    def __init__(self):
        super().__init__("reset", "Resets different aspects or functionalities of the robot.",
                         [DiscreteParameter("aspect", "The aspect to reset.", ["all", "motors", "camera"], "all")])


class RotateCommand(Command):
    def __init__(self):
        super().__init__("rotate", "Rotates the head of the robot.",
                         [ContinuousParameter("horizontal", "Horizontal angle to rotate to. Ranges from -1 (left)"
                                                            " to 1 (right).", -1, 1, 0.5),
                          ContinuousParameter("vertical", "Vertical angle to rotate to. Ranges from -1 (down)"
                                                          " to 1 (up).", -1, 1, 0.5)])


class SetCommand(Command):
    def __init__(self):
        super().__init__("set", "Changes state of a certain aspect of the robot. Toggles functionalities on or off.",
                         [DiscreteParameter("obj", "The object to change the state of.", ["camera", "microphone"],
                                            "camera"),
                          DiscreteParameter("state", "The state to change to.", ["on", "off"], "on")])


class CommandManager:

    def __init__(self, core_controller: CoreController):
        self.commands = {"reset": (self.reset, ResetCommand), "rotate": (self.rotate, RotateCommand),
                         "set": (self.set, SetCommand)}
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
