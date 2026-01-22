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
