from dataclasses import dataclass
from maze import Maze
from maze.core.direction import Direction
from maze.core.navigation import exit_direction
from prompt.is_direction import is_wall as is_wall_direction, is_dead_end, is_exit_direction
from prompt.util import path_length, exit_distance

@dataclass(frozen=True)
class Facts:
    is_wall: bool
    is_exit: bool
    exit_distance: int | None
    path_length: int
    is_dead_end: bool
    out_of_sight: bool

def extract(direction: Direction, maze: Maze) -> Facts:
    is_wall = is_wall_direction(direction, maze)
    is_exit = maze.position == maze.target and direction == exit_direction(maze.target, maze.size)
    e_distance = exit_distance(maze) if is_exit_direction(direction, maze) else None
    p_length = path_length(direction, maze)
    dead_end = is_dead_end(direction, maze)
    out_of_sight = path_length(direction, maze) > maze.sight_depth

    return Facts(
        is_wall=is_wall,
        is_exit=is_exit,
        exit_distance=e_distance,
        path_length=p_length,
        is_dead_end=dead_end,
        out_of_sight=out_of_sight,
    )

