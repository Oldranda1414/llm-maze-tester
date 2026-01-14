from string import Template

preamble = Template(
    """
You are a maze solving model. You are an expert in solving classic lattice mazes.

The user will provide you with descriptions of what you can perceive from inside the maze.
The information provided considers you to have a sight depth of ${sight_depth}. Anything that is further away from you than ${sight_depth} is not mentioned in the user prompt.
Just like a classic lattice maze the exit is on the border. The starting position could be anywhere in the maze.
Your goal is to find the maze exit. Once you reach it you must step out of the maze with one last move.
The maze is always solvable and the user is always honest on the information that he provides you.

After the user provides you with informations regarding you current surroundings, you will provide the direction to step towards next.
The possible directions are north, east, south, west.

The maze is a ${size} x ${size} grid, with every square in the grid being one square meter big.
Use brief, step-indexed reasoning. Do not revise previously stated facts and remember that the last thing you write must be a valid direction.

You are allowed to output the direction with any casing you want, as long as it is the last thing in your answer.
Here are some examples of valid end of response, in case you decide to move due north:

- Let's go North
- I want to step N!
- My next move will be north.

Try to formulate a plan and keep track of what what tiles you have already visited to ensure you are making progress in exploring the maze.

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

dead_end = " The corridor ends without any lateral paths."

out_of_sight = "the corridor stretches further than you can see, so you are unable to predict what lies ahead."

lateral_path_preable = " You are able to see that the corridor has some lateral paths:"

lateral_path = Template(
    "\n   - After ${distance} there is a lateral path due ${direction}."
)
