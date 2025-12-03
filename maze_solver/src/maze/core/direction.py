from enum import Enum

from maze.core.coordinate import Coordinate

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

