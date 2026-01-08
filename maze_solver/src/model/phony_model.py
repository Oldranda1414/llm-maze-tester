import sys
import yaml

from model import Model

from chat_history import ChatHistory, Exchange

DEBUG_SYSTEM_PROMPT = "debug system prompt"


class PhonyModel(Model):
    def __init__(self):
        self._chat_history = ChatHistory(DEBUG_SYSTEM_PROMPT)

    def ask(self, prompt: str, provide_history: bool = True) -> str:
        _ = provide_history  # unused parameter
        move = input(prompt)
        move = move.strip(" ").upper()

        if move == "C":
            sys.exit()

        self._chat_history.add_exchange(Exchange(prompt, move))
        return move

    @property
    def name(self) -> str:
        return "phony_model"

    @property
    def history(self) -> ChatHistory:
        return self._chat_history

    @property
    def system_prompt(self) -> str:
        return DEBUG_SYSTEM_PROMPT

    def set_system_prompt(self, system_prompt: str) -> None:
        _ = system_prompt

    def reset_model(self, system_prompt: str | None = None):
        _ = system_prompt
        self._chat_history = ChatHistory(DEBUG_SYSTEM_PROMPT)

    def save_history(self, filepath: str) -> bool:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.safe_dump(self._chat_history.to_yaml(), f, sort_keys=False)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False
