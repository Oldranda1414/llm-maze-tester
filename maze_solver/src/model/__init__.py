from typing import Protocol

from chat_history import ChatHistory


class Model(Protocol):

    @property
    def history(self) -> ChatHistory: ...

    def ask(self, prompt: str, provide_history: bool = True) -> str: ...

    def reset_history(self): ...

    def save_history(self, filepath: str) -> bool: ...

model_names: list[str] = [
            "llama3",
            "qwen3",
            "smollm2",
            "phi4-mini",
            "deepseek-r1",
            "mistral"
        ]

