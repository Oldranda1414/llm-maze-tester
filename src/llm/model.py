import json

from litellm import completion
from litellm.exceptions import APIConnectionError

from error.model import ModelNameError, ModelNotInstalledError
from error.generation import ModelTimeoutError

from llm.server import get_api_base, get_server_model_name, is_model_installed 
from llm.server import start as start_server

REQUEST_TIMEOUT = 3600

class Model:
    
    def __init__(self, model_name: str):
        if not _is_valid_name(model_name):
            raise ModelNameError(model_name)
        if not is_model_installed(model_name):
            raise ModelNotInstalledError(model_name)

        self.model_name = model_name
        self.chat_history: list[dict[str, str]] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def ask(self, message: str) -> str:
        start_server()
        self.chat_history.append({ "content": message,"role": "user"})
        try:
            response = completion(
                        model = get_server_model_name(self.model_name),
                        messages = self.chat_history,
                        api_base = get_api_base(),
                        request_timeout = REQUEST_TIMEOUT
            )
            self.chat_history.append({ "content": response.choices[0].message.content,"role": "assistant"})
            return response.choices[0].message.content
        except APIConnectionError:
            raise ModelTimeoutError(self.model_name, REQUEST_TIMEOUT)

    def history(self) -> list[dict[str, str]]:
        return self.chat_history

    def reset_history(self):
        self.chat_history = []

    def save_history(self, filepath: str) -> bool:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2)
            print(f"Chat history saved to {filepath}")
            return True
        except (IOError, OSError) as e:
            print(f"Error saving chat history: {str(e)}")
            return False

def _is_valid_name(model_name) -> bool:
    return model_name in model_names

model_names = [
            "llama3",
            #"qwen3",
            #"smollm2",
            #"phi4-mini",
            #"deepseek-r1",
            #"mistral"
        ]
