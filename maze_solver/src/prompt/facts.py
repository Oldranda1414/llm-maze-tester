from dataclasses import dataclass
from copy import deepcopy

from maze import Maze
from maze.core.direction import Direction, get_opposite
from maze.core.navigation import exit_direction
from prompt.is_direction import (
    is_wall as is_wall_direction,
    is_dead_end,
    is_exit_direction,
)
from prompt.util import path_length, exit_distance


@dataclass(frozen=True)
class LateralPath:
    direction: Direction
    distance: int

    def __str__(self) -> str:
        return f"LateralPath: {self.direction}, {self.distance}"

    def __repr__(self) -> str:
        return f"LateralPath: {self.direction}, {self.distance}"


@dataclass(frozen=True)
class Facts:
    is_wall: bool
    is_exit: bool
    exit_distance: int | None
    path_length: int
    is_dead_end: bool
    out_of_sight: bool
    lateral_paths: list[LateralPath] | None


def extract_facts(direction: Direction, maze: Maze) -> Facts:
    is_wall = is_wall_direction(direction, maze)
    is_exit = maze.position == maze.target and direction == exit_direction(
        maze.target, maze.size
    )
    e_distance = exit_distance(maze) if is_exit_direction(direction, maze) else None
    p_length = path_length(direction, maze)
    dead_end = is_dead_end(direction, maze)
    out_of_sight = path_length(direction, maze) > maze.sight_depth
    lateral_paths = _extract_lateral_paths(direction, maze)

    return Facts(
        is_wall=is_wall,
        is_exit=is_exit,
        exit_distance=e_distance,
        path_length=p_length,
        is_dead_end=dead_end,
        out_of_sight=out_of_sight,
        lateral_paths=lateral_paths if len(lateral_paths) > 0 else None,
    )


def _extract_lateral_paths(direction: Direction, maze: Maze) -> list[LateralPath]:
    maze = deepcopy(maze)
    p_lenght = path_length(direction, maze)
    opposite = get_opposite(direction)
    lateral_paths: list[LateralPath] = []
    max_steps = min(p_lenght, maze.sight_depth)
    for i in range(1, max_steps + 1):
        maze.move(direction)
        avail_dirs = maze.available_directions()
        avail_dirs.remove(opposite)
        if direction in avail_dirs:
            avail_dirs.remove(direction)
        found_paths = [LateralPath(avail_dir, i) for avail_dir in avail_dirs]
        if len(found_paths) > 0:
            lateral_paths.extend(found_paths)
    return lateral_paths
