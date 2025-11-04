from dataclasses import dataclass
from move import Coordinate

@dataclass
class ConnectionList:
    vertical: list[list[bool]]
    horizontal: list[list[bool]]

    def __init__(self, vertical: list[list[bool]], horizontal: list[list[bool]]):
        self.vertical = vertical
        self.horizontal = horizontal

    def connected(self, a: Coordinate, b: Coordinate) -> bool:
        """Return True if a and b are directly connected."""
        (r1, c1), (r2, c2) = a, b
        dr, dc = r2 - r1, c2 - c1

        if abs(dr) + abs(dc) != 1:
            return False

        if dr == 1:
            return self.vertical[r1][c1]
        if dr == -1:
            return self.vertical[r2][c2]
        if dc == 1:
            return self.horizontal[r1][c1]
        if dc == -1:
            return self.horizontal[r2][c2]
        return False

    def neighbors_of(self, cell: Coordinate) -> list[Coordinate]:
        """Return all adjacent coordinates connected to cell."""
        r, c = cell
        size = len(self.vertical)
        nbs = []
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
