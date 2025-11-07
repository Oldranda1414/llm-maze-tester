from dataclasses import dataclass
from move import Coordinate, Direction

@dataclass
class ConnectionList:
    vertical: list[list[bool]]
    horizontal: list[list[bool]]

    def __init__(self, vertical: list[list[bool]], horizontal: list[list[bool]]):
        self.vertical = vertical
        self.horizontal = horizontal

    def connected(self, a: Coordinate, b: Coordinate) -> bool:
        """Return True if a and b are adiacent and connected."""
        if a in self.neighbors_of(b):
            return True
        return False

    def neighbors_of(self, cell: Coordinate) -> list[Coordinate]:
        """Return all adjacent cells connected to cell."""
        r, c = cell
        size = len(self.vertical)
        nbs = []
        if r < size and c < size:
            if r > 0 and self.vertical[r - 1][c]:
                nbs.append((r - 1, c))
            if r < size - 1 and self.vertical[r][c]:
                nbs.append((r + 1, c))
            if c > 0 and self.horizontal[r][c - 1]:
                nbs.append((r, c - 1))
            if c < size - 1 and self.horizontal[r][c]:
                nbs.append((r, c + 1))
        return nbs

    def num_neighbors(self, cell: Coordinate) -> int:
        return len(self.neighbors_of(cell))

def direction(start: Coordinate, target: Coordinate) -> Direction | None:
    """
    Returns the direction from start to target if one exists, None otherwise
    """
    (r1, c1), (r2, c2) = start, target
    dr, dc = r2 - r1, c2 - c1

    if dr != 0 and dc != 0:
        return None

    if dr > 0:
        return Direction.SOUTH
    if dr < 0:
        return Direction.NORTH
    if dc > 0:
        return Direction.EAST
    if dc < 0:
        return Direction.WEST

    return None

