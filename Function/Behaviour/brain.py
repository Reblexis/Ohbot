import os
from typing import Dict, Any, List, Generator

import openai
from abc import ABC, abstractmethod

from openai.openai_object import OpenAIObject

from constants import *
from Web.Controls.command_manager import CommandManager


class BrainController(ABC):
    def __init__(self, command_manager: CommandManager):
        self.command_manager = command_manager
        pass

    @abstractmethod
    def process(self, query: dict) -> dict:
        pass


class GPT3BrainController(BrainController):
    API_FILE_PATH = OTHER_FOLDER / "openai_api_key.txt"

    BEHAVIOUR_PROMPT = "You are controlling a robot. Available commands are: `say`, `toggle`, `help`, `pass`." \
                       "If you want to use a command, you should first learn more about it by typing `help [command]`. After this you get response" \
                       "from the system describing the command and its usage. You can then determine if you want to use it or find one that suits you better." \
                       "If you think that doing nothing is the best response, respond with pass and nothing will happen." \
                       "You can only respond with commands and nothing else. Your answer can be as short as you want." \
                       "This is VERY IMPORTANT you can only respond with the commands."

    def __init__(self, command_manager: CommandManager):
        super().__init__(command_manager)
        openai.api_key = open(self.API_FILE_PATH, "r").read()
        self.messages = []
        self.initialize_messages()

    def initialize_messages(self):
        self.messages = [
            {"role": "system", "content": self.BEHAVIOUR_PROMPT},
            {"role": "user", "content": "Hello how are you?"},
            {"role": "assistant", "content": "help say"},
            {"role": "system",
             "content": command_manager.help({"command": "say"})},
            {"role": "assistant", "content": "say --text=\"Hello. I'm doing fine thank you\""},
        ]

    def get_response(self, recursion_counter: int = 0) -> dict[str, str] | dict[str, str | Any]:
        if recursion_counter > 3:
            return {"response": "This is a scripted message. I don't know what to do."}

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        response_content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response_content})
        command = response_content.split(" ")[0]

        print(self.messages)

        if command == "pass":
            return {"response": "pass"}

        if command == "help":
            command = response_content.split(" ")[1]
            system_response = self.command_manager.help({"command": command})
            self.messages.append({"role": "system", "content": system_response})
            return {"response": self.get_response(recursion_counter + 1)}

        is_correct, status_message = self.command_manager.execute_command(response_content)
        if not is_correct:
            self.messages.append({"role": "system", "content": status_message})
            return {"response": self.get_response(recursion_counter + 1)}

        return {"response": response}

    def process(self, query: dict) -> dict:
        spoken_content: str = query["spoken_content"]
        self.messages.append({"role": "user", "content": spoken_content})
        return self.get_response()


if __name__ == "__main__":
    command_manager = CommandManager(None)
    bc = GPT3BrainController(command_manager)
    print(bc.process({"spoken_content": "Please tell me the whole english alphabet from a to z."}))
