from yaspin import yaspin

from model.factory import llm_model


def main():
    model_name = input("model name:\n")
    model = llm_model(model_name)
    system_prompt = input("system prompt:\n")
    model.set_system_prompt(system_prompt)
    while True:
        prompt = input("prompt (Q to quit, B to go back in history):\n")
        if prompt == "Q":
            return
        if prompt == "B":
            history = model.history
            history.chat = history.chat[:-2]
            model._chat_history = history  # type: ignore
            print("Last exchange deleted.")
            print("----Current last response----:")
            print(model.history.chat[-1].response)
        else:
            with yaspin(text="Processing...", color="yellow") as spinner:
                response = model.ask(prompt)
                spinner.ok("")
            print("------Response------:\n", response)


if __name__ == "__main__":
    main()
