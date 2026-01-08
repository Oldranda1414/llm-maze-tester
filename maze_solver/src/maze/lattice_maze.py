from copy import deepcopy
from collections import deque
from functools import cached_property
import yaml

from maze.core.coordinate import Coordinate
from maze.core.direction import Direction, get_offsets
from maze.core.navigation import direction_strict, exit_direction
from maze.core.connection_list import ConnectionList
from maze.output import save_maze, print_maze


class LatticeMaze:
    """
    A class representing a maze with a start and end point.
    """

    def __init__(
        self,
        cl: ConnectionList,
        size: int,
        start: Coordinate,
        target: Coordinate,
        sight_depth: int,
    ):
        self._sight_depth = sight_depth
        self._connection_list = cl
        self._size = size
        self._start = start
        self._target = target
        self._path = [self._start]
        self._decisions: list[Direction] = []
        self._position = self._start
        self._solved = False

    @property
    def size(self) -> int:
        return self._size

    @property
    def start(self) -> Coordinate:
        return self._start

    @property
    def target(self) -> Coordinate:
        return self._target

    @property
    def sight_depth(self) -> int:
        return self._sight_depth

    @property
    def connection_list(self) -> ConnectionList:
        return deepcopy(self._connection_list)

    @property
    def decisions(self) -> list[Direction]:
        return self._decisions

    @property
    def solved(self):
        """Check if the maze is solved.
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self._solved

    @property
    def position(self):
        """Get the current position in the maze.
        Returns:
            Coordinate: The current position (row, column)
        """
        return self._position

    def set_position(self, new_position: Coordinate):
        self._position = new_position

    @property
    def path(self):
        """Get the current path"""
        return deepcopy(self._path)

    def _set_path(self, new_path: list[Coordinate], is_solved: bool = False):
        self._path = new_path
        self._position = new_path[-1]
        self._solved = is_solved

    def move(self, direction: Direction) -> bool:
        if self._solved:
            raise RuntimeError(
                "Maze.move() called on solved maze\nMaze.move() cannot be called on a solved maze!"
            )

        legal_directions = self.available_directions()
        self._decisions.append(direction)
        if self._target == self._position and direction == exit_direction(
            self._target, self._size
        ):
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

    def print(self):
        print_maze(self)

    def save(self, save_path: str):
        save_maze(self, save_path)

    def reset(self):
        self._path = [self._start]
        self._position = self._start
        self._solved = False

    @cached_property
    def solution(self) -> list[Coordinate]:
        """
        Compute the optimal (shortest) path from start to target using BFS.
        Returns:
            list[Coordinate]: the path from start to target, inclusive.
        Raises:
            ValueError: if no path exists.
        """

        start = self._start
        target = self._target
        cl = self._connection_list

        # BFS initialization
        queue = deque([start])
        visited: dict[Coordinate, Coordinate | None] = {start: None}

        while queue:
            current = queue.popleft()

            if current == target:
                break

            for nb in cl.connected_neighbors(current):
                if nb not in visited:
                    visited[nb] = current
                    queue.append(nb)

        # Reconstruct path
        if target not in visited:
            raise ValueError("Maze has no valid path from start to target")

        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = visited[cur]

        return list(reversed(path))

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
            "solved": self.solved,
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
        is_solved = data.get("solved", False)

        maze = cls(connection_list, size, start, target, sight_depth)
        maze._set_path(path, is_solved)

        return maze
