from maze import Maze
from move import Direction

from prompt.util import path_length_str, path_length
from prompt.is_direction import (
        is_exit_direction,
        is_dead_end,
        is_wall,
    )
from prompt.prompts import (
        preamble as preamble_template,
        direction as direction_template,
        corridor as corridor_template,
        wall as wall_prompt,
        exit_prompt,
        exit_found as exit_found_prompt,
        dead_end as dead_end_prompt,
        out_of_sight as out_of_sight_prompt
    )
from prompt.warning import illegal_answer_warning_text, illegal_direction_warning_text
 
def get_preamble(maze: Maze) -> str:
    return preamble_template.substitute(size=maze.size())

def illegal_answer_warning(_: Maze) -> str:
    return illegal_answer_warning_text

def illegal_direction_warning(_: Maze) -> str:
    return illegal_direction_warning_text

def step_prompt(maze: Maze) -> str: 
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    original_path = maze.path()
    step_prompt = ""
    for direction in directions:
        step_prompt += _path_prompt(direction, maze) + "\n"
    maze.set_path(original_path)
    return step_prompt

def _path_prompt(direction: Direction, maze: Maze) -> str:
    prompt = direction_template.substitute(direction=str(direction))
    if is_wall(direction, maze):
        return prompt + wall_prompt
    if is_exit_direction(direction, maze):
        if exit_distance(maze) == 0:
            return prompt + exit_found_prompt
        if exit_distance(maze) <= maze.sight_depth():
            return prompt + exit_prompt
    p_length = path_length_str(direction, maze)
    if path_length(direction, maze) > maze.sight_depth():
        return prompt + out_of_sight_prompt
    prompt += corridor_template.substitute(path_length=p_length)
    if is_dead_end(direction, maze):
        prompt += " " + dead_end_prompt
    return prompt

def exit_distance(maze) -> int:
    p_x, p_y = maze.position()
    t_x, t_y = maze.target()
    if p_x == t_x:
        return abs(p_y - t_y)
    if p_y == t_y:
        return abs(p_x - t_x)
    raise ValueError("maze current position and target are not aligned on one axis, so distance is non trivial")

