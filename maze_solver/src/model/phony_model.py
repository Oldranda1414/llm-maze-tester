import sys
import yaml

from model import Model

from chat_history import ChatHistory, Exchange

debug_system_prompt = "debug system prompt"

class PhonyModel(Model):

    def __init__(self, _: str):
        self.chat_history = ChatHistory(debug_system_prompt)

    def ask(self, prompt: str, provide_history: bool = True) -> str:
        _ = provide_history # unused parameter
        move = input(prompt)
        move = move.strip(" ").upper()

        if move == "C":
            sys.exit()

        self.chat_history.add_exchange(Exchange(prompt, move))
        return move

    @property
    def history(self) -> ChatHistory: return self.chat_history

    def reset_history(self):
        self.chat_history = ChatHistory(debug_system_prompt)

    def save_history(self, filepath: str) -> bool:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.chat_history.to_yaml(), f, sort_keys=False)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False
