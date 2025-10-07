from num2words import num2words

from maze import Coordinate, Direction, Maze

PREAMBLE = """
You are inside a maze. You have a compass with you so you. The maze is well lit so you can see in all directions how long the corridors are.
Both the starting cell and the exit cell are on the border of the grid.
Your goal is to find the maze exit.

Tell me which direction you would like to go to. Provide your answer in the form of the initial of the cardinal direction you wish to take a step forwards to.
The possible directions are N for north, E for east, S for south, W for west.

As an example if you want to step towards north you would answer: N
Remember to provide only the cardinal direction initial in you answer.

You get as many turns as you want, so it's normal that at the start you have not enough information to know on what cell the exit is, so consider exploring to gather information at the start.
"""

PROD_PATH_PREAMBLE = "The last productive moves you have made (aka excluding consecutive opposite moves) are: "
 
def get_preamble(maze: Maze) -> str:
    return PREAMBLE + f"\nThe maze is a {maze.width} x {maze.height} grid, with every square in the grid being one square meter big.\n"

def generate_step_prompt(maze: Maze) -> str: 
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    initial_position = maze.position()
    original_path = maze.path()
    step_prompt = ""
    for direction in directions:
        step_prompt += _get_path_prompt(direction, maze, initial_position) + "\n"
    maze.set_path(original_path)

    return step_prompt

def _get_path_prompt(direction: Direction, maze: Maze, initial_position: Coordinate) -> str:
    path_lenght = _get_path_length(direction, maze, initial_position)
    prompt = f"Due {str(direction)} there is "
    if path_lenght == 0:
        return prompt + "a wall. Seems you can't step in that direction."
    path_lenght_str = _lenght_to_string(path_lenght)
    return prompt + f"a corridor that goes on for {path_lenght_str} meters before encountering a wall."

def _get_path_length(direction: Direction, maze: Maze, initial_position: Coordinate) -> int:
    counter = 0
    while direction in maze.get_directions():
        counter += 1
        maze.move(direction)
    maze.set_position(initial_position)
    return counter

def _prod_path_prompt(maze: Maze) -> str:
    return PROD_PATH_PREAMBLE + ", ".join([decision.to_coordinate() for decision in _productive_path(maze)])
    
def _productive_path(maze: Maze) -> list[Direction]:
    path = maze.decisions().copy()
    productive_path: list[Direction] = []
    opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST
        }
    i = 0
    while i < len(path):
        if i + 1 < len(path) and path[i + 1] == opposites[path[i]]:
            i += 2
        else:
            productive_path.append(path[i])
            i += 1
    return productive_path

def _lenght_to_string(lenght: int) -> str:
    unit = "meter" if lenght == 1 else "meters"
    return f"{num2words(lenght)} {unit}"
