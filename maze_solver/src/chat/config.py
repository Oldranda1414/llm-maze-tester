from dataclasses import dataclass


@dataclass(frozen=True)
class ChatConfig:
    model: str
