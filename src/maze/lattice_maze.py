from copy import deepcopy
import random

from maze_dataset import LatticeMaze as DatasetLatticeMaze

from move import Coordinate, Direction, DIRECTIONS
from maze.output import save_maze, print_maze

class LatticeMaze:
    """
    A class representing a maze with a start and end point.

    args:
        width (int): Width of the maze
        height (int): Height of the maze
        save_path (str): Path to save maze png to
    """
    def __init__(self, maze: DatasetLatticeMaze, save_path: str, seed: int = 42):
        random.seed(seed)
    
        self.maze = maze
        self.size = maze.grid_n
        self.save_path = save_path
        self.target = self._random_border_point(maze)
        start_candidates = [(i,j) for i in range(self.size) for j in range(self.size) if (i,j) != self.target]
        self.start = random.choice(start_candidates)
        self._path = [self.start]
        self._position = self.start

    def _random_border_point(self, maze: DatasetLatticeMaze) -> Coordinate:
        def border_cells():
            return [
                (r, c)
                for r in range(self.size)
                for c in range(self.size)
                if r == 0 or r == self.size - 1 or c == 0 or c == self.size - 1
            ]

        nodes_array = maze.get_nodes()
        accessible: set[tuple[int, int]] = set(map(tuple, nodes_array.tolist())) # type: ignore
        borders = [cell for cell in border_cells() if cell in accessible]
        border_point = random.choice(borders)
        return border_point

    def move(self, direction: Direction) -> bool:
        """Move the current position in the specified direction.
        Args:
            direction (str): The direction to move (U, D, L, R)
        Returns:
            bool: True if the move was successful, False if blocked by a wall
        """
        direction = direction
        if direction not in DIRECTIONS:
            raise ValueError("Invalid direction. Use U, D, L, or R.")

        dr, dc = DIRECTIONS[direction]
        new_pos = (self._position[0] + dr, self._position[1] + dc)
        neighbors: set[Coordinate] = set(map(tuple, self.maze.get_coord_neighbors(self._position))) # type: ignore
        if new_pos in neighbors:
            self._position = new_pos
            self._path.append(new_pos)
            return True
        else:
            print("Move blocked by wall.")
            return False

    def get_directions(self) -> list[Direction]:
        """Get the possible directions to move from the current position.
        Returns:
            list: A list of possible directions (U, D, L, R)
        """
        neighbors: set[Coordinate] = set(map(tuple, self.maze.get_coord_neighbors(self._position))) # type: ignore
        allowed: list[Direction] = []
        for d, (dr, dc) in DIRECTIONS.items():
            new_pos = (self._position[0] + dr, self._position[1] + dc)
            if new_pos in neighbors:
                allowed.append(d)
        return allowed

    def position(self):
        """Get the current position in the maze.
        Returns:
            Coordinate: The current position (row, column)
        """
        return self._position

    def path(self):
        """Get the current path
        """
        return deepcopy(self._path)

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
        return self._position == self.target

    def set_position(self, new_position: Coordinate):
        self._position = new_position

    def set_path(self, new_path: list[Coordinate]):
        self._path = new_path

    def print(self):
        print_maze(self)

    def save(self, save_path: str | None = None):
        save_maze(self, save_path if save_path else self.save_path)

    def reset(self):
        self._path = [self.start]
        self._position = self.start

    def connection_list(self):
        return self.maze.connection_list
