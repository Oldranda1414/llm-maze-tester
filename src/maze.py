"""
maze.py
A simple maze game where the player can navigate through a maze using commands.
The maze is generated using a depth-first search algorithm.
The player can move in four directions: Up (U), Down (D), Left (L), and Right (R).
The maze is represented as a grid of cells, where walls are present between cells.
The player starts at a random position on the border of the maze and must reach the end point.
The maze is displayed using matplotlib, and the player can see their current position and the path taken.
"""
from typing import TypeAlias
from copy import deepcopy
from enum import Enum

import random
import matplotlib.pyplot as plt
import numpy as np
from jaxtyping import Int

from maze_dataset import LatticeMaze
from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.maze import TargetedLatticeMaze

from rich.console import Console
from rich.text import Text

Coordinate: TypeAlias = tuple[int, int]

class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

    def __str__(self):
        conversion: dict[Direction, str] = {
                Direction.NORTH: "North",
                Direction.EAST: "East",
                Direction.SOUTH: "South",
                Direction.WEST: "West"
        }
        return conversion[self]

    def __repr__(self):
        return str(self)

    def to_coordinate(self) -> str:
        conversion: dict["Direction", str] = {
                Direction.NORTH: "N",
                Direction.EAST: "E",
                Direction.SOUTH: "S",
                Direction.WEST: "W"
        }
        return conversion[self]

    @classmethod
    def from_coordinate(cls, coord: str) -> "Direction":
        conversion: dict[str, "Direction"] = {
                "N": cls.NORTH,
                "E": cls.EAST,
                "S": cls.SOUTH,
                "W": cls.WEST
        }
        if coord not in conversion.keys():
            raise ValueError("provided string is not a valid coordinate (N,E,S,W)")
        return conversion[coord]

DIRECTIONS: dict[Direction, Coordinate] = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1)
}

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
    def __init__(self, width: int = 6, height:int = 6, save_path: str | None = "maze.png", plot: bool = True, block_on_plot: bool = True):
        self.width = width
        self.height = height
        self.save_path = save_path
        self.plot = plot
        self.block_on_plot = block_on_plot
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
        """Print the maze with the current path.
        """
        pixels = self._add_path(self.maze.as_pixels())
        if self.plot:
            plt.close('all')
            plt.figure(figsize=(5, 5))
        
            plt.imshow(pixels, cmap='gray')
            plt.title(f"Maze {self.width}x{self.height}")
            plt.axis('off')
            
            if self.save_path:
                plt.savefig(self.save_path, dpi=300, bbox_inches='tight')
            else:
                plt.show(block=self.block_on_plot)
        else:
            console = Console()
            for row in pixels:
                text_line = Text()
                for pixel in row:
                    r, g, b = pixel[:3]
                    text_line.append("  ", style=f"on rgb({r},{g},{b})")  # Two spaces for block
                console.print(text_line)

    def reset(self):
        self._path = [self.start]
        self._position = self.start

    def _add_path(self, pixel_maze: Int[np.ndarray, 'x y rgb']) -> Int[np.ndarray, 'x y rgb']:
        PATH_COLOR = np.array([255, 255, 0], dtype=np.uint8)
        CURRENT_COLOR = np.array([255, 165, 0], dtype=np.uint8)
        result = pixel_maze.copy()
        scaling_factor = 2
        
        for index, coord in enumerate(self._path):
            row, col = coord
            center_row = row * scaling_factor + 1
            center_col = col * scaling_factor + 1
            
            if (0 <= center_row < result.shape[0] and 
                0 <= center_col < result.shape[1]):
                result[center_row, center_col] = PATH_COLOR if (index != len(self._path) - 1) else CURRENT_COLOR
    
        return result
        
