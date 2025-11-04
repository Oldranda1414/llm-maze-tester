from typing import Protocol

from move import Coordinate, Direction
from navigation import ConnectionList

class Maze(Protocol):
    """
    A protocol representing a maze with a start and end point.
    """

    # TODO make these into getter
    size: int
    save_path: str
    start: Coordinate
    target: Coordinate

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

    def position(self) -> Coordinate: ...
    """Get the current position in the maze.
    Returns:
        Coordinate: The current position (row, column)
    """

    def path(self) -> list[Coordinate]: ...
    """Get the current path
    """

    def decisions(self) -> list[Direction]: ...

    def connection_list(self) -> ConnectionList: ...

    def solved(self) -> bool: ...
    """Check if the maze is solved.
    Returns:
        bool: True if the maze is solved, False otherwise
    """

    def set_position(self, new_position: Coordinate) -> None: ...

    def set_path(self, new_path: list[Coordinate]) -> None: ...

    def print(self) -> None: ...

    def save(self, save_path: str | None = None) -> None: ...

    def reset(self) -> None: ...

