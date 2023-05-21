from Function.controller import OhbotController
from Web.Controls.command_manager import CommandManager


class ControlManager:
    def __init__(self):
        self.ohbot_controller = None
        self.command_manager = None

    def connect(self) -> bool:
        """
        Connects to the robot.
        :return: True if the connection was successful, False otherwise.
        """
        print("Connecting to the robot...")
        self.ohbot_controller = OhbotController()
        if self.ohbot_controller.search_connection():
            self.command_manager = CommandManager(self.ohbot_controller)
            return True
        else:
            return False

    def send_command(self, command: str) -> bool:
        status = self.command_manager.execute_command(command)
        return status
