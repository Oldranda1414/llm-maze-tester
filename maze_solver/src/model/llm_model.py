from typing import cast
import yaml

from litellm import completion
from litellm.exceptions import APIConnectionError

from error.model import ModelNameError, PromptTokenLimit
from error.generation import ModelTimeoutError

from model import Model, model_names

from model.server import get_api_base, get_server_model_name, is_model_installed, install_model
from model.server import start as start_server, stop as stop_server
from model.completion_result import CompletionResult

from chat_history import ChatHistory, Exchange

REQUEST_TIMEOUT = 3600
SYSTEM_PROMPT = "You are a helpful assistant."

class LLMModel(Model):

    def __init__(self, model_name: str):
        if not _is_valid_name(model_name):
            raise ModelNameError(model_name)
        if not is_model_installed(model_name):
            install_model(model_name)

        self._name = model_name
        self._chat_history: ChatHistory = ChatHistory(SYSTEM_PROMPT)

    @property
    def name(self) -> str: return self._name

    @property
    def history(self) -> ChatHistory: return self._chat_history

    def ask(self, prompt: str, provide_history: bool = True) -> str:
        start_server()
        messages = self._chat_history.to_list()
        if not provide_history:
            messages = [messages[0]] # keep system prompt
        messages.append({"role": "user", "content": prompt})

        try:
            raw_completion_result = completion(
                        model = get_server_model_name(self._name),
                        messages = messages,
                        api_base = get_api_base(),
                        request_timeout = REQUEST_TIMEOUT,
                        extra_body={"keep_alive": 0},
            )
        except APIConnectionError:
            stop_server()
            raise ModelTimeoutError(self._name, REQUEST_TIMEOUT)
        completion_result = cast(CompletionResult, raw_completion_result)

        _check_prompt_token_limit(completion_result, self._name)
        response = completion_result.choices[0].message.content
        self._chat_history.add_exchange(Exchange(prompt, response))
        stop_server()
        return response

    def reset_history(self):
        self._chat_history = ChatHistory(SYSTEM_PROMPT)

    def save_history(self, filepath: str) -> bool:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self._chat_history.to_yaml(), f, sort_keys=False)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False

def _is_valid_name(model_name) -> bool:
    return model_name in model_names

def _check_prompt_token_limit(completion_result: CompletionResult, model_name: str):
    prompt_tokens = completion_result.usage.prompt_tokens
    if prompt_tokens >= prompt_token_limit[model_name]:
        raise PromptTokenLimit(model_name)

prompt_token_limit: dict[str, int] = {
            "llama3": 4096,
            "deepseek-r1": 4096,
}
