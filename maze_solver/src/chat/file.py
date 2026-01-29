import yaml

from chat.config import ChatConfig


def read_file(path: str) -> str:
    with open(path, "r") as file:
        content = file.read()
        return content


def save_file(path: str, contents: str):
    with open(path, "w", encoding="utf-8") as file:
        file.write(contents)


def load_config(path: str) -> ChatConfig:
    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

        model_value = config.get("model")
        if model_value is None:
            print("Warning: 'model' key not found in YAML file")

        return ChatConfig(model_value)
