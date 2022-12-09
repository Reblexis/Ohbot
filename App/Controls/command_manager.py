import re

from App.WebCommunication import sender

from Function.controller import OhbotController

DEFAULT_ROTATE_ARGS = {"obj": "head", "horizontal": 0.5, "vertical": 0.5}


class CommandManager:
    def __init__(self, ohbot_controller: OhbotController):
        self.commands = {"reset_all": self.reset, "rotate": self.rotate}
        self.ohbot_controller = ohbot_controller

    @staticmethod
    def get_arg(args, key, default):
        if key in args:
            return args[key]
        return default

    def reset(self, args: dict):
        pass

    def rotate(self, args: dict):
        cur_args = DEFAULT_ROTATE_ARGS.copy()
        cur_args.update(args)
        self.ohbot_controller.rotate_head_to(horizontal=float(cur_args["horizontal"]),
                                             vertical=float(cur_args["vertical"]))

    def execute_command(self, command: str):
        # command form should be "command_name arg1_name=arg1_value arg2_name=arg2_value..."
        command_name, *args = command.split(" ")
        try:
            args = {arg.split("=")[0]: arg.split("=")[1] for arg in args}
        except:
            sender.send_error("Invalid command format!")
            return
        if command_name in self.commands:
            sender.hide_error()
            print(f"Executing command {command_name} with args {args}")
            self.commands[command_name](args)
        else:
            sender.send_error(f"Command {command_name} not found!")
