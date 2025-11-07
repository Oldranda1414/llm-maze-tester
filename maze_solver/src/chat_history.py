from enum import Enum
from dataclasses import dataclass, asdict
import yaml

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self):
        return self.value

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

    def __str__(self):
        result = ""
        for i, exchange in enumerate(self.chat):
            result = f"Interaction {i+1}:\n"
            result = f"  Author: {exchange.role}\n"
            result = f"  Content: {exchange.content[:100]}...\n" if len(exchange.content) > 100 else f"  Response: {exchange.content}\n"
        return result

    def to_dict(self):
        return {
            "system_prompt": self.system_prompt,
            "chat": [
                {"role": e.role.value, "content": e.content}
                for e in self.chat
            ],
        }

    def to_yaml(self) -> str:
        """Return the chat serialized as a YAML string."""
        return yaml.safe_dump(self.to_dict(), sort_keys=False)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "ChatHistory":
        """Create a ChatHistory from a YAML string."""
        data = yaml.safe_load(yaml_str)
        chat = [
            Exchange(role=Role(e["role"]), content=e["content"])
            for e in data.get("chat", [])
        ]
        return cls(system_prompt=data["system_prompt"], chat=chat)

