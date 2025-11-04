from maze import Maze
from move import Coordinate, Direction

from prompt.util import lenght_to_string
from prompt.is_direction import is_exit_direction, is_dead_end
from prompt.prompts import (
        preamble as preamble_template,
        direction as direction_template,
        corridor as corridor_template,
        wall as wall_prompt,
        exit_prompt,
        dead_end as dead_end_prompt
    )
from prompt.warning import illegal_answer_warning_text, illegal_direction_warning_text
 
def get_preamble(maze: Maze) -> str:
    return preamble_template.substitute(size=maze.size)

def illegal_answer_warning(_: Maze) -> str:
    return illegal_answer_warning_text

def illegal_direction_warning(_: Maze) -> str:
    return illegal_direction_warning_text

def step_prompt(maze: Maze) -> str: 
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
    prompt = direction_template.substitute(direction=str(direction))
    if path_lenght == 0:
        return prompt + wall_prompt
    path_lenght_str = lenght_to_string(path_lenght)
    prompt += corridor_template.substitute(paht_lenght=path_lenght_str)
    prompt += " " + _wall_state(direction, maze, initial_position)
    return prompt

# TODO put this in is_direction.py and change it to use connection_list
def _path_length(direction: Direction, maze: Maze, initial_position: Coordinate) -> int:
    counter = 0
    while direction in maze.get_directions():
        counter += 1
        maze.move(direction)
    maze.set_position(initial_position)
    return counter

def _wall_state(direction: Direction, maze: Maze, initial_position: Coordinate) -> str:
    path_lenght = _path_length(direction, maze, initial_position)
    if is_exit_direction(direction, initial_position, maze.target, path_lenght):
        return exit_prompt
    if is_dead_end(direction, initial_position, maze.connection_list()):
        return dead_end_prompt
    return ""

