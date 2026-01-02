from model.factory import llm_model

def run():
    """Main function to run the llm-maze-tester."""
    model_name = "deepseek-r1"
    print(f"Initializing model: {model_name}")

    model = llm_model(model_name)

    print("\n--- Testing model COT ---")

    cot_prompt = "I want you to explain quantum physics to me. Think through your process, consider in what order you should explain things and then start explaining"
    print(f"\nPrompt: {cot_prompt}")
    cot_response = model.ask(cot_prompt)
    print(f"Response: {cot_response}")

    print("\n--- Testing model interactions ---")
    model.reset_history()
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

