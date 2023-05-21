from Function.Core.core_controller import CoreController


class ControlManager:
    def __init__(self):
        self.camera_feed = None
        self.core_controller = CoreController()

    def connect(self) -> bool:
        """
        Connects to the robot.
        :return: True if the connection was successful, False otherwise.
        """
        print("Connecting to the robot...")
        if self.core_controller.physical_controller.search_connection():
            return True
        else:
            return False

    def get_camera_feed(self):
        return self.core_controller.vision_controller.gen_frames()

