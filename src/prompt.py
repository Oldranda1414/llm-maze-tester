from num2words import num2words

from maze import Maze
from move import Coordinate, Direction

PREAMBLE = """
You are inside a maze. You have a compass with you. The maze is well lit so you can see in all directions how long the corridors are.
Both the starting cell and the exit cell are on the border of the grid.
Your goal is to find the maze exit.

Tell me which direction you would like to go to. Provide your answer in the form of the initial of the cardinal direction you wish to take a step forwards to.
The possible directions are N for north, E for east, S for south, W for west.

You are advised to think out loud about what your next move should be, but remember that the last thing you write must be a valid direction.

As an example if you want to step towards north the last character in your answer would be: N

You get as many turns as you want, so it's normal that at the start you have not enough information to know on what cell the exit is, so consider exploring to gather information at the start.
"""

PROD_PATH_PREAMBLE = "The last productive moves you have made (aka excluding consecutive opposite moves) are: "

ILLEGAL_ANSWER_WARNING = """
Your last answer did not end with a valid direction.

Remember that your answers must end by providing the direction you want to move to. The valid directions you can provide are N for north, E for east, S for south, W for west.

As an example if you want to step towards north the last character in your answer would be: N
"""

ILLEGAL_DIRECTION_WARNING = """
You walk directly into a wall, hitting your nose. Place more attention on the direcions that are available to you!
"""
 
def preamble(maze: Maze) -> str:
    return PREAMBLE + f"\nThe maze is a {maze.width} x {maze.height} grid, with every square in the grid being one square meter big.\n"

def illegal_answer_warning(_: Maze) -> str:
    return ILLEGAL_ANSWER_WARNING

def illegal_direction_warning(_: Maze) -> str:
    return ILLEGAL_DIRECTION_WARNING

def generate_step_prompt(maze: Maze) -> str: 
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    initial_position = maze.position()
    original_path = maze.path()
    step_prompt = ""
    for direction in directions:
        step_prompt += _path_prompt(direction, maze, initial_position) + "\n"
    maze.set_path(original_path)
    return step_prompt

def _path_prompt(direction: Direction, maze: Maze, initial_position: Coordinate) -> str:
    path_lenght = _path_length(direction, maze, initial_position)
    prompt = f"Due {str(direction)} there is "
    if path_lenght == 0:
        return prompt + "a wall. Seems you can't step in that direction."
    path_lenght_str = _lenght_to_string(path_lenght)
    prompt += f"a corridor that goes on for {path_lenght_str} before encountering a wall."
    prompt += " " + _wall_state(direction, maze, initial_position)
    return prompt

def _path_length(direction: Direction, maze: Maze, initial_position: Coordinate) -> int:
    counter = 0
    while direction in maze.get_directions():
        counter += 1
        maze.move(direction)
    maze.set_position(initial_position)
    return counter

def _wall_state(direction: Direction, maze: Maze, initial_position: Coordinate) -> str:
    path_lenght = _path_length(direction, maze, initial_position)
    for _ in range(path_lenght):
        maze.move(direction)
    available_directions = maze.get_directions()
    maze.set_position(initial_position)
    if len(available_directions) == 1:
        return "It seems to be a dead end."
    return "The path changes direction from there. You should be able to see where the corridor goes if you go up to the wall."

def _lenght_to_string(lenght: int) -> str:
    unit = "meter" if lenght == 1 else "meters"
    return f"{num2words(lenght)} {unit}"
