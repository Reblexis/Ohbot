from Function.Behaviour.behaviour_controller import BehaviourController
from Function.Hearing.hearing_controller import HearingController
from Function.Speech.speech_controller import SpeechController
from Function.Vision.vision_controller import VisionController


class CoreController:
    def __init__(self):
        self.behaviour_controller = BehaviourController()
        self.hearing_controller = HearingController()
        self.speech_controller = SpeechController()
        self.vision_controller = VisionController()

