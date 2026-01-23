import random
from enum import Enum
from dataclasses import dataclass

from maze.core.coordinate import Coordinate


class CellColor(Enum):
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"
    GRAY = "#808080"
    ORANGE = "#FFA500"

    def to_hex(self) -> str:
        return self.value


@dataclass
class ColoredCell:
    coordinate: Coordinate
    color: CellColor

    def to_yaml(self) -> dict:
        """Return a YAML-serializable representation."""
        return {
            "coordinate": list(self.coordinate),
            "color": self.color.name,
        }

    @classmethod
    def from_yaml(cls, data: dict) -> "ColoredCell":
        """Reconstruct a ColoredCell from YAML-loaded data."""
        return cls(
            coordinate=Coordinate(data["coordinate"]),
            color=CellColor[data["color"]],
        )


def random_colored_cells(
    n_mazes: int, maze_size: int, n_colored_cells: int, seed: int = 42
) -> list[list[ColoredCell]]:
    rng = random.Random(seed)
    if n_colored_cells >= len(CellColor):
        raise ValueError(
            f"n_colored_cells cannot be bigger then the available number of colors ({len(CellColor)})"
        )
    colored_cells: list[list[ColoredCell]] = []
    for _ in range(n_mazes):
        colored_cells.append(
            [
                ColoredCell(coord, color)
                for coord in _unique_random_coordinates(maze_size, n_colored_cells, rng)
                for color in rng.sample(set(CellColor), n_colored_cells)
            ]
        )

    return colored_cells


def _unique_random_coordinates(
    max_val: int, n: int, rng: random.Random
) -> list[Coordinate]:
    max_possible_tuples = max_val * max_val
    if n > max_possible_tuples:
        raise ValueError(
            f"Cannot generate {n} unique tuples. "
            f"Maximum possible with max_val={max_val} is {max_possible_tuples}"
        )

    # Use a set to ensure uniqueness
    unique_coordinates = set()

    # Generate tuples until we have n unique ones
    while len(unique_coordinates) < n:
        coordinate_val = (rng.randrange(max_val), rng.randrange(max_val))
        unique_coordinates.add(coordinate_val)

    return list(unique_coordinates)
