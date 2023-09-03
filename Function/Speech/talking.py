import requests
import os
from pydub import AudioSegment
from pydub.playback import play

from constants import *


class TalkingController:
    """
    Talking is currently working via eleven labs API. Therefore, there is a network connection required.
    """

    API_KEY = "b8e30e3ad53288a05e9f5283b67ef6c5"
    VOICE_OPTIONS = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Domi": "AZnzlk1XvdvUeBnXmlld",
        "Bella": "EXAVITQu4vr4xnSDxMaL",
        "Antoni": "ErXwobaYiN019PkySvjV",
        "Elli": "MF3mGyEYCl7XYWbV9V6O",
        "Josh": "TxGEqnHWrfWFTfGW9XjX",
        "Arnold": "VR6AewLTigWG4xSOukaG",
        "Adam": "pNInz6obpgDQGcFmaJgB",
        "Sam": "yoZ06aMxZJJ28mfd3POQ",
    }
    VOICE_ID = VOICE_OPTIONS["Adam"]
    SPEECH_FILE = OTHER_FOLDER / "tts.wav"

    def __init__(self):
        self._headers = {
            "Content-Type": "application/json",
            "xi-api-key": self.API_KEY,
        }
        tts_url = (
            f"https://api.elevenlabs.io/v1/voices"
        )
        response = requests.get(tts_url, headers=self._headers)

    def say(self, text: str) -> bool:
        """Speak text using elevenlabs.io's API
        Args:
            text (str): The text to speak
            voice_index (int, optional): The voice to use. Defaults to 0.
        Returns:
            bool: True if the request was successful, False otherwise
        """
        if text == "":
            return True

        edited_text = text
        tts_url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.VOICE_ID}"
        )
        response = requests.post(tts_url, headers=self._headers, json={"text": text})

        if response.status_code == 200:
            audio_data = response.content
            with open(self.SPEECH_FILE, "wb") as f:
                f.write(audio_data)
            speech = AudioSegment.from_mp3(self.SPEECH_FILE)
            play(speech)
            # os.remove(self.SPEECH_FILE)
            return True

        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.content)
            return False
