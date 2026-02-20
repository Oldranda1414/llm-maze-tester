from typing import Protocol
import random
from functools import cached_property

from maze.color.colored_cell import ColoredCell
from maze.core.direction import Direction
from maze.core.coordinate import Coordinate
from maze.core.connection_list import ConnectionList


class Maze(Protocol):
    """
    A protocol representing a maze with a start and end point.
    """

    @property
    def size(self) -> int: ...

    @property
    def start(self) -> Coordinate: ...

    @property
    def target(self) -> Coordinate: ...

    @property
    def sight_depth(self) -> int: ...

    @property
    def connection_list(self) -> ConnectionList: ...

    @property
    def solved(self) -> bool: ...

    @property
    def position(self) -> Coordinate: ...

    def set_position(self, new_position: Coordinate) -> None: ...

    @property
    def path(self) -> list[Coordinate]: ...

    @property
    def decisions(self) -> list[Direction]: ...

    @property
    def colored_cells(self) -> list[ColoredCell]: ...

    def move(self, direction: Direction) -> bool: ...

    def available_directions(self) -> list[Direction]: ...

    def print(self) -> None: ...

    def save(self, save_path: str, draw_character: bool = True) -> None: ...

    def reset(self) -> None: ...

    @cached_property
    def solution(self) -> list[Coordinate]: ...

    def to_yaml(self) -> str: ...

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "Maze": ...


def generate_target(maze_size: int, rng: random.Random) -> Coordinate:
    border_cells = [
        (r, c)
        for r in range(maze_size)
        for c in range(maze_size)
        if r == 0 or r == maze_size - 1 or c == 0 or c == maze_size - 1
    ]
    borders = [cell for cell in border_cells]
    border_point = rng.choice(borders)
    return border_point


def generate_start(
    maze_size: int, maze_target: Coordinate, rng: random.Random
) -> Coordinate:
    start_candidates = [
        (i, j)
        for i in range(maze_size)
        for j in range(maze_size)
        if (i, j) != maze_target
    ]
    return rng.choice(start_candidates)
