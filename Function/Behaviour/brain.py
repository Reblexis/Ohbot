import json
from typing import Any

import openai
from abc import ABC, abstractmethod

from constants import *
from DataManagment.file_system import ensure_open_ai_api


class BrainController(ABC):
    def __init__(self, command_manager):
        self.command_manager = command_manager
        pass

    @abstractmethod
    def process(self, query: dict) -> dict:
        pass


class GPT3BrainController(BrainController):

    BEHAVIOUR_PROMPT = ("You are controlling a robot. You are responding to a content recognized from user's speech. You can answer with keyword pass if "
                        "you think that the robot should ignore the user's speech or if you have finished your response."
                        " You have available commands which you can use that control the robot. Anything you say (excluding 'pass') will be said by the robot."
                        "Remember you HAVE to use the keyword pass to finish your response.")

    SAVED_MESSAGES_COUNT = 10
    INITIAL_MESSAGE_COUNT = 5

    def __init__(self, command_manager):
        super().__init__(command_manager)
        self.functions = None
        ensure_open_ai_api()
        self.messages = []
        self.functions = command_manager.get_commands_gpt3()
        self.initialize_messages()

    def initialize_messages(self):
        self.messages = [
            {"role": "system", "content": self.BEHAVIOUR_PROMPT},
            {"role": "user", "content": "Assistant. Hello how are you?"},
            {"role": "assistant", "content": "I'm doing well thank you. Pass."},
            {"role": "user", "content": "Assistant. Where"},
            {"role": "assistant", "content": "Pass."},
        ]

    def delete_old_messages(self):
        if len(self.messages) <= self.SAVED_MESSAGES_COUNT + self.INITIAL_MESSAGE_COUNT:
            return

        messages_backup = self.messages.copy()
        self.initialize_messages()
        for message in messages_backup[-self.SAVED_MESSAGES_COUNT:]:
            self.messages.append(message)

    def get_response(self, recursion_counter: int = 0) -> list:
        self.delete_old_messages()

        if recursion_counter > 3:
            return [{"content": "This is a scripted message. I don't know what to do."}]

        print("Answering messages: " + str(self.messages))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            temperature=0,
            messages=self.messages,
            functions=self.functions,
            function_call='auto'
        )
        response_message = response["choices"][0]["message"]
        print(response_message)
        response_content = response_message["content"]
        if response_content is None:
            response_content = ""

        self.messages.append(response_message)
        if response_message.get("function_call"):
            function_feedback: str = self.command_manager.execute_command_gpt3(response_message.get("function_call"))
            self.messages.append({"role": "function", "name": response_message["function_call"]["name"],
                                  "content": function_feedback})

        self.command_manager.say({"text": response_content.replace("Pass", "").replace("pass", "").strip()})

        assistant_responses = [response_content]

        if "pass" in response_content or "Pass" in response_content:
            return assistant_responses

        assistant_responses.extend(self.get_response(recursion_counter + 1))
        return assistant_responses

    def process(self, query: dict) -> list:
        if "spoken_content" not in query:
            return [{"content": "pass"}]

        spoken_content: str = query["spoken_content"]
        self.messages.append({"role": "user", "content": spoken_content})
        responses: list = self.get_response()
        print("Assistant responses:")
        print(responses)
        print("------------------")

        return responses


if __name__ == "__main__":
    command_manager = CommandManager(None)
    bc = GPT3BrainController(command_manager)
    print(bc.process({"spoken_content": "Please turn on the camera"}))
