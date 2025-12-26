from model.factory import llm_model

SYSTEM_PROMPT = "You are a helpful assistant."

print("control case...")
m = llm_model("llama3")

print(m.ask("What is the capital of France?"))
print(m.ask("Can you repeat that?"))

print("testing removing history...")
m = llm_model("llama3")

print(m.ask("What is the capital of France?"))

m.reset_history()

print(m.ask("Can you repeat that?"))
