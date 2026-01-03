from string import Template

preamble = Template(
"""
You are inside a maze. You have a compass with you. The maze is well lit so you can see in all directions how long the corridors are.
Just like a classic maze the exit is on the border. You could be anywhere in the maze as your starting position.
Your goal is to find the maze exit. Once you reach it you must step out of the maze with one last move.

The maze is a ${size} x ${size} grid, with every square in the grid being one square meter big.

You may reason freely and in detail about what your next move should be.
Exploration and careful thinking are encouraged.

However, you MUST always conclude your answer with a final move.

### Output format (mandatory)

First, write your reasoning in plain text.
Then, on a new line, write exactly one line in the following format:

FINAL MOVE: <N|E|S|W>

Nothing is allowed after that line.

### Rules

- You must choose exactly one of: N, E, S, W.
- Do NOT output code, simulations, or examples.
- Do NOT explain the rules of the game.
- Failure to provide a final move in the specified format means failure of the task.

Example:

Reasoning:
I want to explore the unknown corridor to gather more information.

FINAL MOVE: N
"""
)

direction = Template("Due ${direction} ")

corridor = Template("there is a corridor that goes on for ${path_length} before encountering a wall.")

last_move = Template("You move one meter ${direction}\n")

steps_summary = Template("\nThe moves you have made till now are: ${decisions}\n")

step_epilogue = Template("Your possible moves are: ${directions}.\nAfter thinking it through, provide your next move.")

wall = "there is a wall. You can't step in that direction."

exit_prompt = "you can see a natural light shining in that direction, it is probably the direction of the exit!"

exit_found = "you can see the exit in that direction! One last step and you are out of the maze!"

dead_end = " It is a dead end."

out_of_sight = "the corridor stretches further than you can see, so you are unable to predict what lies ahead."

options = " Although the corridor ends with a wall, you notice that some of the lateral paths along the way are open so it isn't a dead end."

