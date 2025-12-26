from typing import Protocol

from chat_history import ChatHistory
from model.llm_model import LLMModel
from model.phony_model import PhonyModel

class Model(Protocol):

    @property
    def history(self) -> ChatHistory: ...

    def ask(self, prompt: str, provide_history: bool = True) -> str: ...

    def reset_history(self): ...

    def save_history(self, filepath: str) -> bool: ...

def llm_model(name: str) -> Model:
    return LLMModel(name)

def phony_model(name: str) -> Model:
    return PhonyModel(name)

model_names: list[str] = [
            "llama3",
            "qwen3",
            "smollm2",
            "phi4-mini",
            "deepseek-r1",
            "mistral"
        ]

