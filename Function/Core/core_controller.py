from Function.Behaviour.behaviour_controller import BehaviourController
from Function.Hearing.hearing_controller import HearingController
from Function.Speech.speech_controller import SpeechController
from Function.Vision.vision_controller import VisionController
from Function.Physical.physical_controller import PhysicalController


class CoreController:
    def __init__(self, command_manager):
        print("INIT CORE CONTROLLER")
        self.behaviour_controller = BehaviourController(command_manager)
        self.hearing_controller = HearingController()
        self.speech_controller = SpeechController()
        self.vision_controller = VisionController()
        self.physical_controller = PhysicalController()

        command_manager.initialize_core_controller(self)

    def run(self):
        while True:
            hearing_info: dict = self.hearing_controller.step()
            if "speech_recognition" in hearing_info and hearing_info["speech_recognition"]["new_content"]:
                print(hearing_info["speech_recognition"])

            self.vision_controller.step()
            self.behaviour_controller.step(hearing_info)
            self.speech_controller.step()
            self.physical_controller.step()
