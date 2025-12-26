from typing import Protocol

class Usage(Protocol):
    prompt_tokens: int

class Message(Protocol):
    content: str

class Choice(Protocol):
    message: Message

class CompletionResult(Protocol):
    usage: Usage
    choices: list[Choice]

