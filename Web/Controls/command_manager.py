import re

from Function.Core.core_controller import CoreController

DEFAULT_ROTATE_ARGS = {"obj": "head", "horizontal": 0.5, "vertical": 0.5}  # Slight rotation to the right and up
DEFAULT_SET_ARGS = {"obj": "camera", "state": "on"}


class CommandManager:
    def __init__(self, core_controller: CoreController):
        self.commands = {"reset_all": self.reset, "rotate": self.rotate, "set": self.set}
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
                self.core_controller.vision_controller.show_camera_feed()
            elif cur_args["state"] == "off" and self.core_controller.vision_controller.show_camera:
                self.core_controller.vision_controller.show_camera = False

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
