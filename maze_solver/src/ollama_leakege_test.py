from chat_history import ChatHistory
from llm.model import Model

SYSTEM_PROMPT = "You are a helpful assistant."

print("control case...")
m = Model("llama3")

print(m.ask("What is the capital of France?"))
print(m.ask("Can you repeat that?"))

print("testing removing history...")
m = Model("llama3")

print(m.ask("What is the capital of France?"))

m.chat_history = ChatHistory(SYSTEM_PROMPT)

print(m.ask("Can you repeat that?"))
