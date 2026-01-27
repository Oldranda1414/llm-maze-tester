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
            updated_history = history.chat[:-2]
            model._chat_history = updated_history
        else:
            response = model.ask(prompt)
            print("Response:\n", response)


if __name__ == "__main__":
    main()
