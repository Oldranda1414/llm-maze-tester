from maze import Maze
from move import Direction

from prompt.util import path_length_str
from prompt.is_direction import (
        is_exit_direction,
        is_dead_end,
        is_wall,
        is_out_of_sight
    )
from prompt.prompts import (
        preamble as preamble_template,
        direction as direction_template,
        corridor as corridor_template,
        wall as wall_prompt,
        exit_prompt,
        dead_end as dead_end_prompt,
        out_of_sight as out_of_sight_prompt
    )
from prompt.warning import illegal_answer_warning_text, illegal_direction_warning_text
 
def get_preamble(maze: Maze) -> str:
    return preamble_template.substitute(size=maze.size)

def illegal_answer_warning(_: Maze) -> str:
    return illegal_answer_warning_text

def illegal_direction_warning(_: Maze) -> str:
    return illegal_direction_warning_text

def step_prompt(maze: Maze, sight_depth: int) -> str: 
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    original_path = maze.path()
    step_prompt = ""
    for direction in directions:
        step_prompt += _path_prompt(direction, maze, sight_depth) + "\n"
    maze.set_path(original_path)
    return step_prompt

def _path_prompt(direction: Direction, maze: Maze, sight_depth: int) -> str:
    prompt = direction_template.substitute(direction=str(direction))
    if is_wall(direction, maze):
        return prompt + wall_prompt
    path_length = path_length_str(direction, maze)
    prompt += corridor_template.substitute(path_length=path_length)
    prompt += " " + _wall_state(direction, maze, sight_depth)
    return prompt

def _wall_state(direction: Direction, maze: Maze, sight_depth: int) -> str:
    if is_out_of_sight(direction, maze, sight_depth):
        return out_of_sight_prompt
    if is_exit_direction(direction, maze):
        return exit_prompt
    if is_dead_end(direction, maze):
        return dead_end_prompt
    return ""

