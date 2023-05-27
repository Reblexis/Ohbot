import numpy as np
import speech_recognition as sr
import io
from scipy.io.wavfile import write
import speech_recognition
import openai
import os

from constants import *
from DataManagment import file_system as fs


class SpeechRecognitionController:
    """
    Transcribes audio to text. Current version is using speech_recognition library combined with whisper for better
    transcription. It works in the following manner:
    1. Recognize smaller chunks of audio using speech_recognition library
    2. If there is a wake word recognized in any of the chunks, start collecting all the following chunks
    3. Stop when the person stops speaking to the robot (currently if not sufficient amount of words are recognized in
     some period of time)
    4. Transcribe the collected chunks using whisper
    """
    WAKE_WORDS = ["tars", "stars", "cars", "bars"]

    SAMPLE_RATE = 16000

    SMALL_CHUNK_SIZE = SAMPLE_RATE * 2
    SMALL_CHUNK_UPDATE = int(SAMPLE_RATE * 0.5)
    assert SMALL_CHUNK_UPDATE <= SMALL_CHUNK_SIZE

    def __init__(self):
        print("Initializing speech recognition controller...")
        self.recognizer = sr.Recognizer()
        fs.ensure_open_ai_api()

        self.short_buffer: list = []  # This buffer is used for wake word recognition and end of speech detection
        self.listening_deep = False
        self.long_buffer: list = []  # This buffer is used to collect all the audio after the wake word is recognized

        print("Speech recognition controller initialized!")

    def receive_chunk(self, chunk: list):
        if self.listening_deep:
            self.long_buffer.append(chunk)

        self.wakeword_buffer.append(chunk)
        self.process_wakeword_buffer()


    def transcribe_google(self, audio: np.array) -> str:
        byte_io = io.BytesIO(bytes())
        write(byte_io, self.sample_rate, audio)
        result_bytes = byte_io.read()
        audio_data = sr.AudioData(result_bytes, self.sample_rate, 2)

        try:
            return self.recognizer.recognize_google(audio_data=audio_data, language="en-US")
        except speech_recognition.UnknownValueError:
            return ""

    def transcribe_path(self, path: Path, precise: bool = False) -> str:
        if precise:
            audio_data = open(path.as_posix(), "rb")
            return openai.Audio.transcribe("whisper-1", audio_data)
        else:
            with sr.AudioFile(path.as_posix()) as source:
                audio = self.recognizer.record(source)
            try:
                return self.recognizer.recognize_google(audio_data=audio, language="en-US")
            except speech_recognition.UnknownValueError:
                return ""
