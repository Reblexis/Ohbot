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

    SMALL_CHUNK_SIZE = 3.000  # Seconds
    SMALL_CHUNK_UPDATE = 1  # Seconds
    assert SMALL_CHUNK_UPDATE <= SMALL_CHUNK_SIZE

    def __init__(self, chunk_sample_rate: int, bytes_per_sample: int):
        print("Initializing speech recognition controller...")
        self.recognizer = sr.Recognizer()
        fs.ensure_open_ai_api()

        self.chunk_sample_rate = chunk_sample_rate
        self.bytes_per_sample = bytes_per_sample  # How many byter are in one value of audio data (4 for float32)
        self.bytes_per_second = self.chunk_sample_rate * self.bytes_per_sample

        self.short_buffer: bytearray = bytearray(b'')  # Used for wake word recognition and end of speech detection
        self.short_buffer_save: bytearray = bytearray(b'')  # Used to save the short buffer to avoid buffer errors
        self.listening_deep = False
        self.long_buffer: bytearray = bytearray(b'')  # Used to collect all the audio after the wake word is recognized

        print("Speech recognition controller initialized!")

    def receive_chunk(self, chunk: bytes):
        if self.listening_deep:
            self.long_buffer.extend(chunk)

        self.short_buffer.extend(chunk)

    def process(self):
        if len(self.short_buffer) >= self.SMALL_CHUNK_SIZE * self.bytes_per_second:
            self.short_buffer_save = self.short_buffer.copy()
            self.short_buffer = self.short_buffer[len(self.short_buffer) -
                                                  int(self.SMALL_CHUNK_UPDATE * self.bytes_per_second):]
            self.process_short_buffer()

            print(len(self.short_buffer))

    def process_short_buffer(self):
        transcription = self.transcribe_sr()
        print(f"Transcription: {transcription}")
        if any(word in transcription for word in self.WAKE_WORDS):
            self.long_buffer.extend(self.short_buffer_save)
            self.listening_deep = True

        if transcription == "" and self.listening_deep:
            self.listening_deep = False
            self.process_long_buffer()
            self.long_buffer = bytearray(b'')

    def process_long_buffer(self):
        transcription = self.transcribe_whisper()
        print(f"Transcription WHISPER: {transcription}")

    def transcribe_sr(self) -> str:
        data = np.frombuffer(self.short_buffer_save, dtype=np.float32)
        data = fs.resample_audio(data, self.chunk_sample_rate, self.SAMPLE_RATE)

        audio_int = (data * 32768).astype(np.int16)
        byte_io = io.BytesIO(bytes())
        write(byte_io, self.SAMPLE_RATE, audio_int)
        result_bytes = byte_io.read()
        audio_data = sr.AudioData(result_bytes, self.SAMPLE_RATE, 2)

        print("Transcribing...")
        try:
            return self.recognizer.recognize_google(audio_data=audio_data, language="en-US")
        except speech_recognition.UnknownValueError:
            return ""

    def transcribe_whisper(self) -> str:
        audio_data = np.frombuffer(self.long_buffer, dtype=np.float32)
        audio_data = fs.resample_audio(audio_data, self.chunk_sample_rate, self.SAMPLE_RATE)
        fs.save_to_file(audio_data, Path("long_buffer.wav"), additional_info={"type": "audio", "sample_rate": 16000})
        audio_data = open("long_buffer.wav", "rb")
        return openai.Audio.transcribe("whisper-1", audio_data)

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
