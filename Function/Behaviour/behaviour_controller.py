from Function.Behaviour.brain import GPT3BrainController


class BehaviourController:
    """
    This class is the abstract class representing the behaviour of the agent.
    At the moment it only contains the interaction with the brain.
    """
    def __init__(self, command_manager):
        self.brain_controller = GPT3BrainController(command_manager)

    def step(self, hearing_info: dict):
        important_information = {}
        if "speech_recognition" in hearing_info and hearing_info["speech_recognition"]["new_content"] and hearing_info["speech_recognition"][
            "long_transcription"] != "":
            important_information["spoken_content"] = hearing_info["speech_recognition"]["long_transcription"]

        self.brain_controller.process(important_information)
