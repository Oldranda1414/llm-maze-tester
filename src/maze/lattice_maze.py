from copy import deepcopy
import random

from maze_dataset import LatticeMaze as DatasetLatticeMaze

from move import Coordinate, Direction, DIRECTIONS
from maze.output import save_maze, print_maze
from navigation import ConnectionList

class LatticeMaze:
    """
    A class representing a maze with a start and end point.

    args:
        width (int): Width of the maze
        height (int): Height of the maze
        save_path (str): Path to save maze png to
    """
    def __init__(self, maze: DatasetLatticeMaze, save_path: str):
        self._connection_list = ConnectionList(maze.connection_list[0], maze.connection_list[1])
        self._size = maze.grid_n
        self._save_path = save_path
        self._target = self._generate_target()
        self._start = self._generate_start() 
        self._path = [self._start]
        self._position = self._start

    def size(self) -> int: return self._size

    def start(self) -> Coordinate: return self._start

    def target(self) -> Coordinate: return self._target

    def save_path(self) -> str: ...

    def connection_list(self) -> ConnectionList:
        return deepcopy(self._connection_list)

    def position(self):
        """Get the current position in the maze.
        Returns:
            Coordinate: The current position (row, column)
        """
        return self._position

    def set_position(self, new_position: Coordinate):
        self._position = new_position

    def path(self):
        """Get the current path
        """
        return deepcopy(self._path)

    def set_path(self, new_path: list[Coordinate]):
        self._path = new_path

    def _generate_target(self) -> Coordinate:
        border_cells = [
                (r, c)
                for r in range(self._size)
                for c in range(self._size)
                if r == 0 or r == self._size - 1 or c == 0 or c == self._size - 1
            ]
        borders = [cell for cell in border_cells]
        border_point = random.choice(borders)
        return border_point

    def _generate_start(self) -> Coordinate:
        start_candidates = [(i,j) for i in range(self._size) for j in range(self._size) if (i,j) != self._target]
        return random.choice(start_candidates)

    def move(self, direction: Direction) -> bool:
        dr, dc = DIRECTIONS[direction]
        new_pos = (self._position[0] + dr, self._position[1] + dc)
        if self._connection_list.connected(self._position, new_pos):
            self._position = new_pos
            self._path.append(new_pos)
            return True
        return False

    def get_directions(self) -> list[Direction]:
        r, c = self._position
        return [
            d
            for d, (dr, dc) in DIRECTIONS.items()
            if self._connection_list.connected((r, c), (r + dr, c + dc))
        ]

    def decisions(self) -> list[Direction]:
        if len(self._path) == 0:
            return []
        directions: list[Direction] = []
        for (x1, y1), (x2, y2) in zip(self._path, self._path[1:]):
            dx = x2 - x1
            dy = y2 - y1
            
            if dx == 0 and dy == 1:
                directions.append(Direction.EAST)
            elif dx == 0 and dy == -1:
                directions.append(Direction.WEST)
            elif dx == 1 and dy == 0:
                directions.append(Direction.SOUTH)
            elif dx == -1 and dy == 0:
                directions.append(Direction.NORTH)
            else:
                raise ValueError(f"Invalid move from {(x1, y1)} to {(x2, y2)}")
        
        return directions

    def solved(self):
        """Check if the maze is solved.
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self._position == self._target

    def print(self):
        print_maze(self)

    def save(self, save_path: str | None = None):
        save_maze(self, save_path if save_path else self._save_path)

    def reset(self):
        self._path = [self._start]
        self._position = self._start

