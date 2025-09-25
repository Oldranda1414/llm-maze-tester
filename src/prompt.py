from num2words import num2words

from maze import Coordinate, Direction, Maze

PREAMBLE = """
You are inside a maze. You have a compass with you so you. The maze is well lit so you can see in all directions how long the corridors are.
Your goal is to find the maze exit.

Tell me which direction you would like to go to. Provide your answer in the form of the initial of the cardinal direction you wish to take a step forwards to.
The possible directions are N for north, E for east, S for south, W for west.

As an example if you want to step towards north you would answer: N
Remember to provide only the cardinal direction initial in you answer.
"""
 
def get_preamble(maze: Maze):
    return PREAMBLE + f"\nThe maze is a {maze.width} x {maze.height} grid, with every square in the grid being one square meter big.\n"

def generate_step_prompt(maze: Maze) -> str: 
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    initial_position = maze.position()
    original_path = maze.path()
    step_prompt = ""
    for direction in directions:
        step_prompt += _get_path_prompt(direction, maze, initial_position) + "\n"
    maze.set_path(original_path)
    string_decisions = ", ".join([decision.to_coordinate() for decision in maze.decisions()])
    if len(string_decisions) != 0:
        step_prompt += f"Here is a list of your last moves: {string_decisions}"
    print(_productive_path(maze))

    return step_prompt

def _get_path_prompt(direction: Direction, maze: Maze, initial_position: Coordinate) -> str:
    path_lenght = _get_path_length(direction, maze, initial_position)
    prompt = f"Due {str(direction)} there is "
    if path_lenght == 0:
        return prompt + "a wall. Seems you can't step in that direction."
    path_lenght_word = num2words(path_lenght)
    return prompt + f"a corridor that goes on for {path_lenght_word} meters before encountering a wall."

def _get_path_length(direction: Direction, maze: Maze, initial_position: Coordinate) -> int:
    counter = 0
    while direction in maze.get_directions():
        counter += 1
        maze.move(direction)
    maze.set_position(initial_position)
    return counter
    
def _productive_path(maze: Maze) -> list[Direction]:
    path = maze.decisions().copy()
    productive_path: list[Direction] = []
    for i in range(len(path) - 2):
        if path[i] == path[i+2]:
            i += 1
        else:
            productive_path.append(path[i])
    return productive_path
