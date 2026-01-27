from typing import Protocol

from chat_history import ChatHistory


class Model(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def history(self) -> ChatHistory: ...

    @property
    def system_prompt(self) -> str: ...

    def set_system_prompt(self, system_prompt: str) -> None: ...

    def ask(self, prompt: str, provide_history: bool = True) -> str: ...

    def reset_model(self, system_prompt: str | None = None): ...

    def save_history(self, filepath: str) -> bool: ...


model_names: list[str] = [
    "llama3",
    "qwen3",
    "smollm2",
    "phi4-mini",
    "deepseek-r1",
    "deepseek-r1:14b",
    "deepseek-r1:32b",
    "mistral",
    "glm-4.7-flash",
    "yi",
]
