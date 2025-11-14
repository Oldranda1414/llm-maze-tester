from copy import deepcopy

import yaml
from maze.core.coordinate import Coordinate
from maze.core.direction import Direction, get_offsets
from maze.core.navigation import direction_strict, exit_direction
from maze.core.connection_list import ConnectionList
from maze.output import save_maze, print_maze

class LatticeMaze:
    """
    A class representing a maze with a start and end point.

    args:
        width (int): Width of the maze
        height (int): Height of the maze
        save_path (str): Path to save maze png to
    """
    def __init__(self, cl: ConnectionList, size: int, start: Coordinate, target: Coordinate, sight_depth: int):
        self._sight_depth = sight_depth
        self._connection_list = cl
        self._size = size
        self._start = start
        self._target = target
        self._path = [self._start]
        self._decisions = []
        self._position = self._start
        self._solved = False

    def size(self) -> int: return self._size

    def start(self) -> Coordinate: return self._start

    def target(self) -> Coordinate: return self._target

    def sight_depth(self) -> int: return self._sight_depth

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
        self._position = new_path[-1]

    def move(self, direction: Direction) -> bool:
        legal_directions = self.available_directions()
        self._decisions.append(direction)
        if self._target == self._position and direction == exit_direction(self._target, self._size):
            self._solved = True
            return True
        if direction in legal_directions:
            dr, dc = get_offsets(direction)
            new_pos = (self._position[0] + dr, self._position[1] + dc)
            self._position = new_pos
            self._path.append(new_pos)
            return True
        return False

    def available_directions(self) -> list[Direction]:
        neighbors = self._connection_list.connected_neighbors(self._position)
        d = [direction_strict(self._position, n) for n in neighbors]
        if self._target == self._position:
            d.append(exit_direction(self._target, self._size))
        return d

    def decisions(self) -> list[Direction]:
        return self._decisions

    def solved(self):
        """Check if the maze is solved.
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self._solved

    def print(self):
        print_maze(self)

    def save(self, save_path: str):
        save_maze(self, save_path)

    def reset(self):
        self._path = [self._start]
        self._position = self._start
        self._solved = False

    def to_yaml(self) -> str:
        """Return the maze serialized as a YAML string."""
        data = {
            "horizontal": self._connection_list.horizontal_passages,
            "vertical": self._connection_list.vertical_passages,
            "start": list(self._start),
            "target": list(self._target),
            "path": [list(p) for p in self._path],
            "sight_depth": self._sight_depth,
            "size": self._size,
        }
        return yaml.safe_dump(data, sort_keys=False)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "LatticeMaze":
        """Reconstruct a Maze from a YAML string."""
        data = yaml.safe_load(yaml_str)

        connection_list = ConnectionList(
            horizontal_passages=[list(row) for row in data["horizontal"]],
            vertical_passages=[list(row) for row in data["vertical"]],
        )

        start = Coordinate(data["start"])
        target = Coordinate(data["target"])
        path = [Coordinate(p) for p in data.get("path", [])]
        sight_depth = data.get("sight_depth", 0)
        size = data.get("size", 0)

        maze = cls(connection_list, size, start, target, sight_depth)
        maze.set_path(path)

        return maze

