import pyttsx3


class TalkingController:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
