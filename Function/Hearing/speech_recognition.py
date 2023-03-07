import whisper
import torch

from constants import *


class SpeechRecognition:
    """
    Transcribes audio to text. Current version is using whisper library developed by OpenAI.
    """

    MODEL_VERSION = "tiny.en"

    def __init__(self):
        self.model = whisper.load_model(self.MODEL_VERSION).to(DEVICE)

    def transcribe(self, audio: torch.Tensor) -> str:
        print("transcribing...")
        transcript = whisper.transcribe(model=self.model, audio=audio)
        print("transcribed!")
        return transcript
