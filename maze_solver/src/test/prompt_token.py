from model.factory import llm_model

def run():
    model = llm_model("deepseek-r1")
    prompt = "something"
    try:
        while(len(prompt) != 100000):
            model.ask(prompt)
            prompt += prompt
    except Exception:
        print(len(prompt))

