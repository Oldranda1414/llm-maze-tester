""" llm-maze-tester entry point """

from llm.model import Model

def main():
    """Main function to run the llm-maze-tester."""
    print("Testing LLM model wrapper...")

    # Create a model instance with a lightweight model for testing
    # Using llama2 as it's commonly available, but you can change to any model you prefer
    model_name = "llama3"
    print(f"Initializing model: {model_name}")

    model = Model(model_name)

    # Test with some simple prompts
    print("\n--- Testing model interactions ---")

    # First interaction
    prompt1 = "What is the capital of France?"
    print(f"\nPrompt: {prompt1}")
    response1 = model.ask(prompt1)
    print(f"Response: {response1}")

    # Second interaction that builds on the first
    prompt2 = "What is another famous city in this country?"
    print(f"\nPrompt: {prompt2}")
    response2 = model.ask(prompt2)
    print(f"Response: {response2}")

    # Display history
    print("\n--- Chat History ---")
    history = model.history()
    print(history)

    # Save history to file
    save_path = "chat_history.json"
    print(f"\nSaving chat history to {save_path}")
    success = model.save_history(save_path)
    if success:
        print("History saved successfully!")
    else:
        print("Failed to save history.")

if __name__ == "__main__":
    main()
