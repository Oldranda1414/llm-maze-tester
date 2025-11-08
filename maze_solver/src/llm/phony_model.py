import sys
import yaml

from chat_history import ChatHistory, Exchange

debug_system_prompt = "debug system prompt"

class Model():

    def __init__(self, _: str):
        self.chat_history = ChatHistory(debug_system_prompt)

    def ask(self, prompt: str) -> str:

        prompt = "give me a move (C to close, Q to save): "
        move = input(prompt)
        move = move.strip(" ").upper()
        coordinates = ["N", "E", "S", "W"]
        actions = ["C"]
        while move not in coordinates + actions:
            print("invalid move try again")
            move = input(prompt)

        if move == "C":
            sys.exit()

        self.chat_history.add_exchange(Exchange(prompt, move))
        return move

    def history(self) -> ChatHistory:
        return self.chat_history

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
