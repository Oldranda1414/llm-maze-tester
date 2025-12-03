from enum import Enum

from maze.core.coordinate import Coordinate
from maze.core.navigation import direction_strict

class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

    def __str__(self) -> str:
        conversion: dict[Direction, str] = {
                Direction.NORTH: "North",
                Direction.EAST: "East",
                Direction.SOUTH: "South",
                Direction.WEST: "West"
        }
        return conversion[self]

    def __repr__(self):
        return str(self)

    def to_coordinate(self) -> str:
        conversion: dict["Direction", str] = {
                Direction.NORTH: "N",
                Direction.EAST: "E",
                Direction.SOUTH: "S",
                Direction.WEST: "W"
        }
        return conversion[self]

    @classmethod
    def from_coordinate(cls, coord: str) -> "Direction":
        conversion: dict[str, "Direction"] = {
                "N": cls.NORTH,
                "E": cls.EAST,
                "S": cls.SOUTH,
                "W": cls.WEST
        }
        if coord not in conversion.keys():
            raise ValueError("provided string is not a valid coordinate (N,E,S,W)")
        return conversion[coord]

def get_offsets(direction: Direction) -> Coordinate:
    DIRECTION_OFFSETS: dict[Direction, Coordinate] = {
        Direction.NORTH: (-1, 0),
        Direction.EAST: (0, 1),
        Direction.SOUTH: (1, 0),
        Direction.WEST: (0, -1)
    }
    return DIRECTION_OFFSETS[direction]

def path_to_directions(path: list[Coordinate]) -> list[Direction]:
    """
    Convert a path (list of Coordinates) into a list of Directions.
    Each consecutive pair of coordinates must be adjacent.

    Args:
        path: List of coordinates forming a valid path.

    Returns:
        List of Directions representing the steps.

    Raises:
        ValueError: if two consecutive coordinates are not adjacent.
    """
    if len(path) < 2:
        return []

    directions: list[Direction] = []

    for a, b in zip(path, path[1:]):
        try:
            d = direction_strict(a, b)
        except ValueError:
            raise ValueError(
                f"Invalid path: coordinates {a} and {b} are not adjacent."
            ) from None

        directions.append(d)

    return directions

