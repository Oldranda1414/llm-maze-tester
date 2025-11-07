from string import Template

preamble = Template(
"""
You are inside a maze. You have a compass with you. The maze is well lit so you can see in all directions how long the corridors are.
Both the starting cell and the exit cell are on the border of the grid.
Your goal is to find the maze exit.

Tell me which direction you would like to go to. Provide your answer in the form of the initial of the cardinal direction you wish to take a step forwards to.
The possible directions are N for north, E for east, S for south, W for west.

You are advised to think out loud about what your next move should be, but remember that the last thing you write must be a valid direction.

As an example if you want to step towards north the last character in your answer would be: N

You get as many turns as you want, so it's normal that at the start you have not enough information to know on what cell the exit is, so consider exploring to gather information at the start.

The maze is a ${size} x ${size} grid, with every square in the grid being one square meter big.
"""
)

direction = Template("Due ${direction} ")

corridor = Template("there is a corridor that goes on for ${path_length} before encountering a wall.")

wall = "there is a wall. Seems you can't step in that direction."

exit_prompt = "you can see a natural light shining in that direction, it is probably the exit!"

dead_end = " It seems to be a dead end."

out_of_sight = "the corridor streatches further than you can see, so you are unable to predict what lies ahead."
