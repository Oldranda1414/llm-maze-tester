from yaspin import yaspin

from chat.file import load_config, read_file
from model.factory import llm_model

CONFIG_PATH = "./chat/config.yaml"
SYSTEM_PROMPT_PATH = "./chat/system_prompt.txt"
PROMPT_PATH = "./chat/prompt.txt"


def main():
    config = load_config(CONFIG_PATH)
    model = llm_model(config.model)
    system_prompt = read_file(SYSTEM_PROMPT_PATH)
    model.set_system_prompt(system_prompt)
    while True:
        user_command = input(
            "Provide command (Q to quit, B to go back in history) or <enter> to execute next step:\n"
        )
        if user_command == "Q":
            return
        if user_command == "B":
            history = model.history
            history.chat = history.chat[:-2]
            model._chat_history = history  # type: ignore
            print("Last exchange deleted.")
            print("----Current last response----:")
            print(model.history.chat[-1].response)
        else:
            with yaspin(text="Processing...", color="yellow") as spinner:
                prompt = read_file(PROMPT_PATH)
                response = model.ask(prompt)
                spinner.ok("")
            print("------Response------:\n", response)
