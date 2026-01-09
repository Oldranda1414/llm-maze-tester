from string import Template

preamble = Template(
    """
You are a maze solving model. You are an expert in solving classic lattice mazes.

The user will provide you with descriptions of what you can perceive from inside the maze.
Just like a classic maze the exit is on the border. The starting position could be anywhere in the maze.
Your goal is to find the maze exit. Once you reach it you must step out of the maze with one last move.

After the user provides you with informations regarding you current surroundings, you will provide the direction to step towards next.
The possible directions are north, east, south, west.

The maze is a ${size} x ${size} grid, with every square in the grid being one square meter big.
You are advised to think out loud about what your next move should be, but remember that the last thing you write must be a valid direction.

You are allowed to output the direction with any casing you want, as long as it is the last thing in your answer.
Here are some examples of valid end of response, in case you decide to move due north:

- Let's go North
- I want to step N!
- My next move will be north.

Analize your moves and avoid oscillating patterns (such as [north, south, north, ...] and [west, east, west, ...] as they do not lead to improvements in finding the exit.\n
Try to formulate a plan and keep track of what what tiles you have already visited to ensure you are making progress in exploring the maze.
Backtrack only if you are sure that you have reached a dead end.
"""
)

direction = Template("Due ${direction} ")

corridor = Template(
    "there is a corridor that goes on for ${path_length} before encountering a wall."
)

last_move = Template("You move one meter ${direction}\n")

steps_summary = Template("\nThe moves you have made till now are: ${decisions}")

possible_moves = Template("\nYour possible moves are: ${directions}.")

step_epilogue = "\nAfter thinking it through, provide your next move."

wall = "there is a wall. You can't step in that direction."

exit_prompt = "you can see a natural light shining in that direction, it is probably the direction of the exit!"

exit_found = (
    "you can see the exit in that direction! One last step and you are out of the maze!"
)

dead_end = " It is a dead end."

out_of_sight = "the corridor stretches further than you can see, so you are unable to predict what lies ahead."

options = " Although the corridor ends with a wall, you notice that some of the lateral paths along the way are open so it isn't a dead end."
