from yaspin import yaspin

from chat.file import load_config, read_file, save_file
from model import Model
from model.factory import llm_model

CONFIG_PATH = "./chat/config.yaml"
SYSTEM_PROMPT_PATH = "./chat/system_prompt.txt"
PROMPT_PATH = "./chat/prompt.txt"
SAVE_HISTORY_PATH = "./chat/saved_history.yaml"


def main():
    config = load_config(CONFIG_PATH)
    model = llm_model(config.model)
    system_prompt = read_file(SYSTEM_PROMPT_PATH)
    model.set_system_prompt(system_prompt)
    print("----loaded system prompt----:")
    print(model.system_prompt)
    while True:
        user_command = input(
            "Provide command (Q to quit, B to go back in history, S to save chat history)\nor <enter> to execute next step:\n"
        )
        if user_command == "Q":
            return
        if user_command == "B":
            back(model)
        if user_command == "S":
            save_history(model)
        else:
            next_step(model)


def back(model: Model):
    if len(model.history.chat) > 0:
        history = model.history
        history.chat = history.chat[:-2]
        model._chat_history = history  # type: ignore
        print("Last exchange deleted.")
        if len(model.history.chat) > 0:
            print("----Current last response----:")
            print(model.history.chat[-1].response)
        else:
            print("Exchange history is currently empty")
            print("----System prompt----:")
            print(model.system_prompt)
    else:
        print("Exchange history is currently empty")
        print("----System prompt----:")
        print(model.system_prompt)


def next_step(model: Model):
    with yaspin(text="Processing...", color="yellow") as spinner:
        prompt = read_file(PROMPT_PATH)
        response = model.ask(prompt)
        spinner.ok("")
    print("------Response------:\n", response)


def save_history(model: Model):
    save_file(SAVE_HISTORY_PATH, model.history.to_yaml())
