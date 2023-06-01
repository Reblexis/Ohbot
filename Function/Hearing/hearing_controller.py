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
    LISTENING_RATE = 44100
    LISTENER_CHUNK_SIZE = 1024 * 4

    def __init__(self):
        print("Initializing hearing controller...")
        self.buffer = None
        self.stream = None
        self.last_buffer_length = 0
        self.p = pyaudio.PyAudio()
        self.to_process = None

        self.speech_recognition_pipeline = speech_recognition_.SpeechRecognitionController(self.LISTENING_RATE, 4)
        print("Hearing controller initialized!")

    def start_listening(self):
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.LISTENING_RATE,
                                  input=True,
                                  frames_per_buffer=self.LISTENER_CHUNK_SIZE,
                                  stream_callback=self.listen,
                                  input_device_index=7)
        self.stream.start_stream()

    def listen(self, in_data, frame_count, time_info, flag):
        self.speech_recognition_pipeline.receive_chunk(in_data)

        return in_data, pyaudio.paContinue

    def step(self):
        speech_recognition_info = self.speech_recognition_pipeline.process()


if __name__ == "__main__":
    hc = HearingController()
    hc.start_listening()


