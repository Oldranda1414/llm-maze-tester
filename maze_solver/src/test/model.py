from maze.factory import create_maze
from model.factory import llm_model
from prompt import PromptGenerator
from prompt.style.narrative import NarrativeStyle

def run():
    """Main function to run the llm-maze-tester."""
    model_name = "deepseek-r1"
    print(f"Initializing model: {model_name}")

    model = llm_model(model_name)

    print("\n--- Testing model COT ---")

    prompt_gen = PromptGenerator(NarrativeStyle())
    maze = create_maze()
    prompt = prompt_gen.get_preamble(maze) + prompt_gen.step_prompt(maze)
    print(f"\nPrompt: {prompt}")
    response = model.ask(prompt)
    print(f"Response: {response}")

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

