import eel

from App.WebCommunication import sender
from App.Controls.command_manager import CommandManager
from Function.controller import OhbotController


class Receiver:
    def __init__(self):
        self.command_manager = None
        self.ohbot_controller = None

    def check_connection(self) -> bool:
        return self.ohbot_controller is not None

    def connect(self):
        self.ohbot_controller = OhbotController()
        if self.ohbot_controller.search_connection():
            self.command_manager = CommandManager(self.ohbot_controller)
            sender.switch_to_console()
            sender.hide_error()
        else:
            sender.send_error("Ohbot not found!")

    def execute_command(self, command: str):
        if not self.check_connection():
            return

        self.command_manager.execute_command(command)


receiver = Receiver()


@eel.expose  # Expose this function to Javascript
def python_log(x):
    print(x)


@eel.expose
def pass_buffer(buffer):
    print(type(buffer))


@eel.expose
def connect():
    receiver.connect()


@eel.expose
def send_command(command):
    receiver.execute_command(command)


@eel.expose
def answer_key_press(key):
    if key == 13:
        print("Enter")


"""

say_hello_py('Python World!')
eel.next_picture('Python World!')   # Call a Javascript function
"""
