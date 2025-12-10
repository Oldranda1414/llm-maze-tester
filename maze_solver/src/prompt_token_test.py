from llm.model import Model

def main():
    model = Model("llama3")
    prompt = "something"
    while(len(prompt) != 100000):
        model.ask(prompt)
        prompt += prompt

if __name__ == "__main__":
    main()

