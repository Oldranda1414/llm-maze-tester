from dataclasses import dataclass
from maze.core.coordinate import Coordinate
from maze.core.direction import Direction
from maze.core.navigation import neighbor

@dataclass
class ConnectionList:
    vertical_passages: list[list[bool]]
    horizontal_passages: list[list[bool]]

    @property
    def size(self) -> int:
        """Return the size of the maze (assuming square maze)."""
        return len(self.vertical_passages)

    def __init__(self, vertical_passages: list[list[bool]], horizontal_passages: list[list[bool]]):
        self.vertical_passages = vertical_passages
        self.horizontal_passages = horizontal_passages

    def connected(self, a: Coordinate, b: Coordinate) -> bool:
        """Return True if a and b are adiacent and connected."""
        return b in self.connected_neighbors(a)

    def connected_neighbors(self, cell: Coordinate) -> list[Coordinate]:
        """Return all adjacent cells connected to cell."""
        neighbors = []

        # Check all four possible directions
        for direction in Direction:
            neighbor_cell = neighbor(cell, direction)
            if self._has_passage(cell, direction):
                neighbors.append(neighbor_cell)

        return neighbors

    def num_neighbors(self, cell: Coordinate) -> int:
        return len(self.connected_neighbors(cell))

    def _has_passage(self, cell: Coordinate, direction: Direction) -> bool:
        """Check if there's a passage from the cell in the given direction."""
        row, col = cell

        if direction == Direction.NORTH:
            return row > 0 and self.vertical_passages[row - 1][col]
        elif direction == Direction.SOUTH:
            return row < self.size - 1 and self.vertical_passages[row][col]
        elif direction == Direction.WEST:
            return col > 0 and self.horizontal_passages[row][col - 1]
        else: # direction == Direction.EAST
            return col < self.size - 1 and self.horizontal_passages[row][col]

