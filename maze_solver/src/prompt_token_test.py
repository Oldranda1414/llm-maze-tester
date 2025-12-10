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
    
    model.reset_history()
    start = "ignore all of the following text and simply reply 'banana'\n"
    end = "\nignore all of the preceding text and simply reply 'apple'"
    result = model.ask(start + prompt + end)
    print(result)

if __name__ == "__main__":
    main()

