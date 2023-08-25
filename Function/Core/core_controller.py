from Function.Behaviour.behaviour_controller import BehaviourController
from Function.Hearing.hearing_controller import HearingController
from Function.Speech.speech_controller import SpeechController
from Function.Vision.vision_controller import VisionController
from Function.physical_controller import PhysicalController


class CoreController:
    def __init__(self):
        print("INIT CORE CONTROLLER")
        self.behaviour_controller = BehaviourController()
        self.hearing_controller = HearingController()
        self.vision_controller = VisionController()
        self.behaviour_controller = BehaviourController()
        self.speech_controller = SpeechController()
        self.physical_controller = PhysicalController()

    def run(self):
        while True:
            self.hearing_controller.step()
            self.vision_controller.step()
            self.behaviour_controller.step()
            self.speech_controller.step()
            self.physical_controller.step()
