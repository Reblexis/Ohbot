import numpy as np
import speech_recognition as sr
import io
from scipy.io.wavfile import write
import speech_recognition

from constants import *


class SpeechRecognitionController:
    """
    Transcribes audio to text. Current version is using speech_recognition library.
    """

    def __init__(self):
        print("Initializing speech recognition controller...")
        self.recognizer = sr.Recognizer()
        print("Speech recognition controller initialized!")

    def transcribe(self, audio: np.array, sample_rate=16000) -> str:
        byte_io = io.BytesIO(bytes())
        write(byte_io, sample_rate, audio)
        result_bytes = byte_io.read()
        audio_data = sr.AudioData(result_bytes, sample_rate, 2)

        try:
            return self.recognizer.recognize_google(audio_data=audio_data, language="en-US")
        except speech_recognition.UnknownValueError:
            return ""
