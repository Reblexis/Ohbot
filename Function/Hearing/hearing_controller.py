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
        self.listening = False
        self.buffer = None
        self.stream = None
        self.last_buffer_length = 0
        self.p = pyaudio.PyAudio()
        self.to_process = None

        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.LISTENING_RATE,
                                  input=True,
                                  frames_per_buffer=self.LISTENER_CHUNK_SIZE,
                                  stream_callback=self.listen,
                                  input_device_index=8)

        self.speech_recognition_pipeline = speech_recognition_.SpeechRecognitionController(self.LISTENING_RATE, 4)
        print("Hearing controller initialized!")

    def find_available_device(self):
        info = self.p.get_host_api_info_by_index(0)

        for i in range(0, info.get('deviceCount')):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

    def listen(self, in_data, frame_count, time_info, flag):
        if not self.listening:
            return in_data, pyaudio.paContinue

        print(self.listening)
        self.speech_recognition_pipeline.receive_chunk(in_data)

        return in_data, pyaudio.paContinue

    def step(self):
        speech_recognition_info = self.speech_recognition_pipeline.process()
        if self.listening:
            print(speech_recognition_info)

    def enable(self):
        print("Enabling hearing controller...")
        self.listening = True

    def disable(self):
        self.listening = False


if __name__ == "__main__":
    hc = HearingController()
    hc.enable()


