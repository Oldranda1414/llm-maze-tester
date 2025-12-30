import sys
import yaml

from model import Model

from chat_history import ChatHistory, Exchange

DEBUG_SYSTEM_PROMPT = "debug system prompt"

class PhonyModel(Model):

    def __init__(self, _: str):
        self._chat_history = ChatHistory(DEBUG_SYSTEM_PROMPT)

    def ask(self, prompt: str, provide_history: bool = True) -> str:
        _ = provide_history # unused parameter
        move = input(prompt)
        move = move.strip(" ").upper()

        if move == "C":
            sys.exit()

        self._chat_history.add_exchange(Exchange(prompt, move))
        return move

    @property
    def name(self) -> str: return "phony_model"

    @property
    def history(self) -> ChatHistory: return self._chat_history

    def reset_history(self):
        self._chat_history = ChatHistory(DEBUG_SYSTEM_PROMPT)

    def save_history(self, filepath: str) -> bool:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self._chat_history.to_yaml(), f, sort_keys=False)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False
