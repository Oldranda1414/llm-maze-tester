"""
maze.py
A simple maze game where the player can navigate through a maze using commands.
The maze is generated using a depth-first search algorithm.
The player can move in four directions: Up (U), Down (D), Left (L), and Right (R).
The maze is represented as a grid of cells, where walls are present between cells.
The player starts at a random position on the border of the maze and must reach the end point.
The maze is displayed using matplotlib, and the player can see their current position and the path taken.
"""
from copy import deepcopy

import random
import numpy as np

from maze_dataset import LatticeMaze
from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.maze import TargetedLatticeMaze

from move import Coordinate, Direction, DIRECTIONS
from maze.output import save_maze, print_maze

class Maze:
    """
    A class representing a maze with a start and end point.
    The maze is generated using a depth-first search algorithm.

    args:
        width (int): Width of the maze
        height (int): Height of the maze
        plot (bool): Whether to plot the maze using matplotlib
        block_on_plot (bool): Whether to block execution until the plot is closed
    """
    def __init__(self, width: int = 6, height:int = 6, save_path: str = "maze.png"):
        if width < 2 or height < 2:
            raise ValueError("maze width and height must be >= 2")
        self.width = width
        self.height = height
        self.save_path = save_path
        lattice_maze: LatticeMaze = LatticeMazeGenerators.gen_dfs(
            np.array([height, width])
        )
        self.start, self.end = self._random_border_points(lattice_maze)
        self.maze = TargetedLatticeMaze.from_lattice_maze(
            lattice_maze,
            self.start,
            self.end
        )
        self._path = [self.start]
        self._position = self.start

    def _random_border_points(self, maze: LatticeMaze) -> tuple[Coordinate, Coordinate]:
        def border_cells():
            return [
                (r, c)
                for r in range(self.height)
                for c in range(self.width)
                if r == 0 or r == self.height - 1 or c == 0 or c == self.width - 1
            ]

        nodes_array = maze.get_nodes()
        accessible: set[tuple[int, int]] = set(map(tuple, nodes_array.tolist())) # type: ignore
        borders = [cell for cell in border_cells() if cell in accessible]
        start = random.choice(borders)
        end = random.choice([b for b in borders if b != start])
        return start, end

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
        return self._position == self.end

    def set_position(self, new_position: Coordinate):
        self._position = new_position

    def set_path(self, new_path: list[Coordinate]):
        self._path = new_path

    def print(self):
        print_maze(self.maze, self._path)

    def save(self, save_path: str | None = None):
        save_maze(self.maze, self._path, save_path if save_path else self.save_path)

    def reset(self):
        self._path = [self.start]
        self._position = self.start

