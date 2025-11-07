from typing import Protocol

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

    def save_path(self) -> str: ...

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

    def get_directions(self) -> list[Direction]: ...
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

    def save(self, save_path: str | None = None) -> None: ...

    def reset(self) -> None: ...

