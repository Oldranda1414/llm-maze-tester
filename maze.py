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

import random
import matplotlib.pyplot as plt
import numpy as np
import maze_dataset as md

from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.plotting import MazePlot
from maze_dataset.maze import TargetedLatticeMaze#, SolvedMaze

Coordinate: TypeAlias = tuple[int, int]

DIRECTIONS: dict[str, Coordinate] = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

class Maze:
    """
    A class representing a maze with a start and end point.
    The maze is generated using a depth-first search algorithm.
    """
    def __init__(self, width: int = 6, height:int = 6, plot: bool = True, block_on_plot: bool = True):
        self.width = width
        self.height = height
        self.plot = plot
        self.block_on_plot = block_on_plot
        lattice_maze: md.LatticeMaze = LatticeMazeGenerators.gen_dfs( # type: ignore
            np.array([height, width])
        )
        self.start, self.end = self._random_border_points(lattice_maze)
        self.maze: TargetedLatticeMaze = TargetedLatticeMaze.from_lattice_maze( # type: ignore
            lattice_maze,
            self.start,
            self.end
        )
        self._path = [self.start]
        self._position = self.start

    def _random_border_points(self, maze: md.LatticeMaze) -> tuple[Coordinate, Coordinate]:
        def border_cells():
            return [
                (r, c)
                for r in range(self.height)
                for c in range(self.width)
                if r == 0 or r == self.height - 1 or c == 0 or c == self.width - 1
            ]

        nodes_array = maze.get_nodes() # type: ignore
        accessible: set[tuple[int, int]] = set(map(tuple, nodes_array.tolist())) # type: ignore
        borders = [cell for cell in border_cells() if cell in accessible]
        start = random.choice(borders)
        end = random.choice([b for b in borders if b != start])
        return start, end

    def move(self, direction: str):
        """Move the current position in the specified direction.
        Args:
            direction (str): The direction to move (U, D, L, R)
        """
        direction = direction.upper()
        if direction not in DIRECTIONS:
            raise ValueError("Invalid direction. Use U, D, L, or R.")

        dr, dc = DIRECTIONS[direction]
        new_pos = (self._position[0] + dr, self._position[1] + dc)
        neighbors: set[Coordinate] = set(map(tuple, self.maze.get_coord_neighbors(self._position))) # type: ignore
        if new_pos in neighbors:
            self._position = new_pos
            self._path.append(new_pos)
        else:
            print("Move blocked by wall.")

    def get_directions(self) -> list[str]:
        """Get the possible directions to move from the current position.
        Returns:
            list: A list of possible directions (U, D, L, R)
        """
        neighbors: set[Coordinate] = set(map(tuple, self.maze.get_coord_neighbors(self._position))) # type: ignore
        allowed: list[str] = []
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

    def solved(self):
        """Check if the maze is solved.
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self._position == self.end

    # seems to not work for now
    # def solve(self):
    #     self.maze: SolvedMaze = SolvedMaze.from_targeted_lattice_maze(self.maze)

    def print(self):
        """Print the maze with the current path.
        """
        if self.plot:
            plt.close('all')
            MazePlot(self.maze).add_predicted_path(self._path).plot() # type: ignore
            plt.show(block=self.block_on_plot) # type: ignore
        else:
            ascii_maze: str = MazePlot(self.maze).add_predicted_path(self._path).to_ascii() # type: ignore
            print(ascii_maze)
