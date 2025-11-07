from enum import Enum
from dataclasses import dataclass, asdict
import yaml

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class Exchange:
    role: Role
    content: str

@dataclass
class ChatHistory:
    system_prompt: str
    chat: list[Exchange]

    def __init__(self, system_prompt: str, chat: list[Exchange] = []):
        self.system_prompt = system_prompt
        self.chat = chat

    def add_user_message(self, content: str):
        self.chat.append(Exchange(Role.USER, content))

    def add_assistant_message(self, content: str):
        self.chat.append(Exchange(Role.ASSISTANT, content))

    def to_dict(self):
        return {
            "system_prompt": self.system_prompt,
            "chat": [asdict(e) for e in self.chat],
        }

    def save_yaml(self, path: str):
        with open(path, "w") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=False)

    @classmethod
    def load_yaml(cls, path: str):
        with open(path) as f:
            data = yaml.safe_load(f)
        chat = [Exchange(**e) for e in data["chat"]]
        return cls(system_prompt=data["system_prompt"], chat=chat)

