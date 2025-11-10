from string import Template

preamble = Template(
"""
You are inside a maze. You have a compass with you. The maze is well lit so you can see in all directions how long the corridors are.
Just like a classic maze the exit is on the border. You could be anywhere in the maze as your starting position.
Your goal is to find the maze exit. Once you reach it you must step out of the maze with one last move.

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

last_move = Template("You move one meter ${direction}\n")

wall = "there is a wall. Seems you can't step in that direction."

exit_prompt = "you can see a natural light shining in that direction, it is probably the direction of the exit!"

exit_found = "you can see the exit in that direction! One last step and you are out of the maze!"

dead_end = " It seems to be a dead end."

out_of_sight = "the corridor streatches further than you can see, so you are unable to predict what lies ahead."

options = " Althogh the corridor ends with a wall, you notice that some of the lateral paths along the way are open so it isn't a dead end."
