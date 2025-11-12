from typing import Protocol
import random

from move import Coordinate, Direction
from maze.navigation import ConnectionList

class Maze(Protocol):
    """
    A protocol representing a maze with a start and end point.
    """

    def size(self) -> int: ...

    def start(self) -> Coordinate: ...

    def target(self) -> Coordinate: ...

    def sight_depth(self) -> int: ...

    def connection_list(self) -> ConnectionList: ...

    def position(self) -> Coordinate: ...
    """Get the current position in the maze.
    Returns:
        Coordinate: The current position (row, column)
    """

    def set_position(self, new_position: Coordinate) -> None: ...

    def path(self) -> list[Coordinate]: ...
    """Get the current path
    """

    def set_path(self, new_path: list[Coordinate]) -> None: ...

    def decisions(self) -> list[Direction]: ...

    def move(self, direction: Direction) -> bool: ...
    """Move the current position in the specified direction.
    Args:
        direction (str): The direction to move (U, D, L, R)
    Returns:
        bool: True if the move was successful, False if blocked by a wall
    """

    def available_directions(self) -> list[Direction]: ...
    """Get the possible directions to move from the current position.
    Returns:
        list: A list of possible directions (U, D, L, R)
    """

    def solved(self) -> bool: ...
    """Check if the maze is solved.
    Returns:
        bool: True if the maze is solved, False otherwise
    """

    def print(self) -> None: ...

    def save(self, save_path: str) -> None: ...

    def reset(self) -> None: ...

    def to_yaml(self) -> str: ...

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "Maze": ...

def generate_target(maze_size) -> Coordinate:
    border_cells = [
            (r, c)
            for r in range(maze_size)
            for c in range(maze_size)
            if r == 0 or r == maze_size - 1 or c == 0 or c == maze_size - 1
        ]
    borders = [cell for cell in border_cells]
    border_point = random.choice(borders)
    return border_point

def generate_start(maze_size: int, maze_target: Coordinate) -> Coordinate:
    start_candidates = [(i,j) for i in range(maze_size) for j in range(maze_size) if (i,j) != maze_target]
    return random.choice(start_candidates)
