from llm.model import Model

def main():
    model = Model("llama3")
    prompt = "something"
    try:
        while(len(prompt) != 100000):
            model.ask(prompt)
            prompt += prompt
    except Exception:
        print(len(prompt))

    model = Model("qwen3")
    model.ask("something")

if __name__ == "__main__":
    main()

