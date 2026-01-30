import yaml
from copy import deepcopy

from ollama import chat, RequestError

from error.model import ModelNameError, ModelNotInitializedError
from error.generation import ModelRequestError

from model import Model, model_names

from model.server import is_model_installed, install_model
from model.server import start as start_server

from chat_history import ChatHistory, Exchange


class LLMModel(Model):
    def __init__(self, model_name: str):
        if not _is_valid_name(model_name):
            raise ModelNameError(model_name)
        if not is_model_installed(model_name):
            install_model(model_name)

        self._name = model_name
        self._system_prompt: str | None = None
        self._chat_history: ChatHistory | None = None
        start_server()

    @property
    def name(self) -> str:
        return self._name

    @property
    def history(self) -> ChatHistory:
        if self._chat_history is None:
            raise ModelNotInitializedError(self.name)
        return deepcopy(self._chat_history)

    @property
    def system_prompt(self) -> str:
        if self._system_prompt is None:
            raise ModelNotInitializedError(self.name)
        return self._system_prompt

    def set_system_prompt(self, system_prompt: str) -> None:
        self._system_prompt = system_prompt
        self._chat_history = ChatHistory(system_prompt)

    def ask(self, prompt: str, provide_history: bool = True) -> str:
        if self._chat_history is None:
            raise ModelNotInitializedError(self.name)

        messages = list(self._chat_history.to_list())
        if not provide_history:
            messages = [messages[0]]  # keep system prompt
        messages.append({"role": "user", "content": prompt})

        try:
            chat_response = chat(
                model=self._name,
                messages=messages,
                think=False,
                stream=False,
            )
        except RequestError as e:
            raise ModelRequestError(self._name) from e
        response = chat_response.message.content or ""
        self._chat_history.add_exchange(Exchange(prompt, response))
        return response

    def reset_model(self, system_prompt: str | None = None):
        if self._system_prompt is None:
            raise ModelNotInitializedError(self.name)
        if system_prompt is not None:
            self._system_prompt = system_prompt
        self._chat_history = ChatHistory(self._system_prompt)

    def save_history(self, filepath: str) -> bool:
        if self._chat_history is None:
            raise ModelNotInitializedError(self.name)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.safe_dump(self._chat_history.to_yaml(), f, sort_keys=False)
            return True
        except (IOError, OSError):
            return False


def _is_valid_name(model_name: str) -> bool:
    return model_name in model_names
