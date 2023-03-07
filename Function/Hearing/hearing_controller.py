import pyaudio
import numpy as np
from pathlib import Path
import torch

from constants import *
from DataManagment import file_system as fs
from Function.Hearing import speech_recognition_


class HearingController:
    LISTENING_RATE = 16000
    LISTENER_CHUNK_SIZE = 1024 * 4
    MAX_BUFFER_LENGTH = 40000
    NEW_BUFFER_LENGTH = 20000

    def __init__(self):
        print("Initializing hearing controller...")
        self.buffer = None
        self.stream = None
        self.last_buffer_length = 0
        self.p = pyaudio.PyAudio()
        self.to_process = None

        self.speech_recognition_pipeline = speech_recognition_.SpeechRecognitionController()
        print("Hearing controller initialized!")

    def start_listening(self):
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=16000,
                                  input=True,
                                  frames_per_buffer=self.LISTENER_CHUNK_SIZE,
                                  stream_callback=self.listen)
        self.stream.start_stream()

    def listen(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        self.buffer = concatenate(self.buffer, audio_data)

        if self.buffer.shape[0] >= self.last_buffer_length + self.NEW_BUFFER_LENGTH:
            fs.save_to_file(self.buffer, Path("test.wav"), additional_info={"type": "audio", "sample_rate": 16000})
            self.buffer = self.buffer[max(self.buffer.shape[0] - self.MAX_BUFFER_LENGTH, 0):]

            self.to_process = self.buffer

            self.buffer = self.buffer[max(0, len(self.buffer) - self.MAX_BUFFER_LENGTH):]
            self.last_buffer_length = len(self.buffer)

        return in_data, pyaudio.paContinue

    def process_buffer(self):
        print("Processing buffer...")
        audio_int = (self.to_process * 32768).astype(np.int16)
        print(np.max(audio_int))
        print(f"Transcribed speech:{self.speech_recognition_pipeline.transcribe(audio_int)}")


def concatenate(a, b):
    if a is None:
        return b
    return np.concatenate([a, b])


