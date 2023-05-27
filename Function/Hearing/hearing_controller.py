import os

import pyaudio
import numpy as np
from pathlib import Path
import torch
import openai

from constants import *
from DataManagment import file_system as fs
from Function.Hearing import speech_recognition_


class HearingController:
    LISTENING_RATE = 16000
    LISTENER_CHUNK_SIZE = 1024 * 4

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
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=self.LISTENER_CHUNK_SIZE,
                                  stream_callback=self.listen,
                                  input_device_index=7)
        self.stream.start_stream()
        while True:
            if self.to_process is not None:
                self.process_buffer()
                self.to_process = None

    def listen(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        self.process_chunk(audio_data)

        return in_data, pyaudio.paContinue

    def process_audio_chunk(self, audio_chunk):
        print("Processing buffer...")

        audio_int = (self.to_process * 32768).astype(np.int16)

        transcription = self.speech_recognition_pipeline.transcribe(audio_int, sample_rate=44100)
        print(transcription)


if __name__ == "__main__":
    hc = HearingController()
    hc.start_listening()


