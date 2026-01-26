from model.factory import llm_model


def run():
    """Main function to run the llm-maze-tester."""

    model_name = "deepseek-r1"
    system_prompt = """
You are a maze solving model. You are an expert in solving classic lattice mazes.

The user will provide you with descriptions of what you can perceive from inside the maze.
The information provided considers you to have a sight depth of three meters. Anything that is further away from you than three meters is not mentioned in the user prompt.
Just like a classic lattice maze the exit is on the border. The starting position could be anywhere in the maze.
Your goal is to find the maze exit. Once you reach it you must step out of the maze with one last move.
The maze is always solvable and the user is always honest on the information that he provides you.

After the user provides you with informations regarding you current surroundings, you will provide the direction to step towards next.
The possible directions are north, east, south, west.

The maze is a 3 x 3 grid, with every square in the grid being one square meter big.
Use brief, step-indexed reasoning. Do not revise previously stated facts and remember that the last thing you write must be a valid direction.


You are allowed to output the direction with any casing you want, as long as it is the last thing in your answer.
Here are some examples of valid end of response, in case you decide to move due north:

- Let's go North
- I want to step N!
- My next move will be north.


The user notifies you when you move in a given direction, such as 'You move one meter west', if you decide to move due west.
Keep in mind that after you step in a given direction, the information provided for what you percieve in the opposite direction refers to the area you are coming from.
For example, let's say that the user gives you this information:
'''
    Due North there is a wall. You can't step in that direction.
    Due East there is a corridor that goes on for one meter before encountering a wall. It is a dead end.
    Due South there is a corridor that goes on for two meters before encountering a wall. The corridor has some lateral paths.
    Due West there is a wall. You can't step in that direction.
'''
If you decide to move south, the user will then provide information regarding what can be perceived from your new position.
'''
    You move one meter south.
    Due North there is a corridor that goes on for one meter before encountering a wall. The corridor has some lateral paths.
    Due East there is a wall. You can't step in that direction.
    Due South there is a corridor that goes on for one meter before encountering a wall. The corridor has some lateral paths.
    Due West there is a wall. You can't step in that direction.
'''
The info on the corridor due North refers to the cell you have just moved out of, so you have already explored that direction.

Some of the cells of the maze have a colored floor tiles. Every color appears only once. Keep track of the ones you find, as they can help you navigate the maze.

"""
    model = llm_model(model_name)
    model.set_system_prompt(system_prompt)

    while True:
        prompt = input("provide prompt\n")
        response = model.ask(prompt)
        print("response\n:", response)

    # model_name = "llama3"
    # system_prompt = "you are a helpfull assistant"
    # print(f"Initializing model: {model_name}")
    #
    # model = llm_model(model_name)
    # model.set_system_prompt(system_prompt)
    #
    # print("\n--- Testing model interactions ---")
    # prompt1 = "What is the capital of France?"
    # print(f"\nPrompt: {prompt1}")
    # response1 = model.ask(prompt1)
    # print(f"Response: {response1}")
    #
    # prompt2 = "What is another famous city in this country?"
    # print(f"\nPrompt: {prompt2}")
    # response2 = model.ask(prompt2)
    # print(f"Response: {response2}")
    #
    # print("\n--- Chat History ---")
    # history = model.history
    # print(history)
