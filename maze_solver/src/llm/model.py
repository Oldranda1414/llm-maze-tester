import yaml

from litellm import completion
from litellm.exceptions import APIConnectionError

from error.model import ModelNameError, ModelNotInstalledError
from error.generation import ModelTimeoutError

from llm.server import get_api_base, get_server_model_name, is_model_installed, install_model
from llm.server import start as start_server

from chat_history import ChatHistory, Exchange

REQUEST_TIMEOUT = 3600
SYSTEM_PROMPT = "You are a helpful assistant."

class Model:
    
    def __init__(self, model_name: str):
        if not _is_valid_name(model_name):
            raise ModelNameError(model_name)
        if not is_model_installed(model_name):
            install_model(model_name)
            raise ModelNotInstalledError(model_name)

        self.model_name = model_name
        self.chat_history: ChatHistory = ChatHistory("You are a helpful assistant.")

    def ask(self, prompt: str) -> str:
        start_server()
        try:
            messages = self.chat_history.to_list()
            messages.append({"role": "user", "content": prompt})
            response = completion(
                        model = get_server_model_name(self.model_name),
                        messages = messages,
                        api_base = get_api_base(),
                        request_timeout = REQUEST_TIMEOUT
            )
            self.chat_history.add_exchange(Exchange(prompt, response.choices[0].message))
            return response.choices[0].message.content
        except APIConnectionError:
            raise ModelTimeoutError(self.model_name, REQUEST_TIMEOUT)

    def history(self) -> ChatHistory:
        return self.chat_history

    def reset_history(self):
        self.chat_history = ChatHistory(SYSTEM_PROMPT)

    def save_history(self, filepath: str) -> bool:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.chat_history.to_yaml(), f, sort_keys=False)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False

def _is_valid_name(model_name) -> bool:
    return model_name in model_names

model_names = [
            "llama3",
            "qwen3",
            "smollm2",
            "phi4-mini",
            "deepseek-r1",
            "mistral"
        ]
