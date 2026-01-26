from enum import Enum
from dataclasses import dataclass

from maze.core.coordinate import Coordinate


class CellColor(Enum):
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFDD00"
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"
    GRAY = "#808080"
    ORANGE = "#FFA500"

    def __str__(self) -> str:
        conversion: dict[CellColor, str] = {
            CellColor.WHITE: "white",
            CellColor.BLACK: "black",
            CellColor.RED: "red",
            CellColor.GREEN: "green",
            CellColor.BLUE: "blue",
            CellColor.YELLOW: "yellow",
            CellColor.CYAN: "cyan",
            CellColor.MAGENTA: "magenta",
            CellColor.GRAY: "gray",
            CellColor.ORANGE: "orange",
        }
        return conversion[self]

    def __repr__(self):
        return str(self)

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
