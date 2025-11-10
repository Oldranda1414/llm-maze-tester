from enum import Enum
from dataclasses import dataclass
import yaml

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self):
        return self.value

@dataclass
class Exchange:
    prompt: str
    response: str

@dataclass
class ChatHistory:
    system_prompt: str
    chat: list[Exchange]

    def __init__(self, system_prompt: str, chat: list[Exchange] = []):
        self.system_prompt = system_prompt
        self.chat = chat

    def add_exchange(self, exchange: Exchange):
        self.chat.append(exchange)

    def to_string(self) -> str:
        result = f"System prompt: {self.system_prompt}\n"
        for i, exchange in enumerate(self.chat):
            result += f"Interaction {i+1}:\n"
            result += f"  Prompt: {exchange.prompt}\n"
            result += f"  Response: {exchange.response}\n"
        return result

    def __str__(self):
        result = f"System prompt: {self.system_prompt}\n"
        for i, exchange in enumerate(self.chat):
            result += f"Interaction {i+1}:\n"
            result += f"  Prompt: {exchange.prompt[:100]}...\n" if len(exchange.response) > 100 else f"  Prompt: {exchange.prompt}\n"
            result += f"  Content: {exchange.response[:100]}...\n" if len(exchange.response) > 100 else f"  Content: {exchange.response}\n"
        return result

    def to_list(self) -> list[dict[str, str]]:
        l = [{"role": "system", "content": self.system_prompt}]
        for exchange in self.chat:
            l.append({"role": "user", "content": exchange.prompt})
            l.append({"role": "assistant", "content": exchange.response})
        return l

    def to_dict(self):
        return {
            "system_prompt": self.system_prompt,
            "chat": [
                {"prompt": e.prompt, "response": e.response}
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
            Exchange(prompt=e["prompt"], response=e["response"])
            for e in data.get("chat", [])
        ]
        return cls(system_prompt=data["system_prompt"], chat=chat)


