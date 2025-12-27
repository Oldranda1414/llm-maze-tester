from model.factory import llm_model

def run():
    """Main function to run the llm-maze-tester."""
    print("Testing LLM model wrapper...")

    model_name = "llama3"
    print(f"Initializing model: {model_name}")

    model = llm_model(model_name)

    print("\n--- Testing model interactions ---")

    prompt1 = "What is the capital of France?"
    print(f"\nPrompt: {prompt1}")
    response1 = model.ask(prompt1)
    print(f"Response: {response1}")

    prompt2 = "What is another famous city in this country?"
    print(f"\nPrompt: {prompt2}")
    response2 = model.ask(prompt2)
    print(f"Response: {response2}")

    print("\n--- Chat History ---")
    history = model.history
    print(history)

