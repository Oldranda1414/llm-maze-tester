import random
import matplotlib.pyplot as plt
import numpy as np
from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.plotting import MazePlot
from maze_dataset.maze import TargetedLatticeMaze, SolvedMaze

DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

class Maze:
    def __init__(self, width=6, height=6, plot=True):
        self.width = width
        self.height = height
        self.plot = plot
        lattice_maze = LatticeMazeGenerators.gen_dfs(
            np.array([height, width])
        )
        self.start, self.end = self._random_border_points(lattice_maze)
        self.maze = TargetedLatticeMaze.from_lattice_maze(
            lattice_maze,
            self.start,
            self.end
        )
        self.path_ = [self.start]
        self.position_ = self.start

    def _random_border_points(self, maze):
        def border_cells():
            return [
                (r, c)
                for r in range(self.height)
                for c in range(self.width)
                if r == 0 or r == self.height - 1 or c == 0 or c == self.width - 1
            ]

        accessible = set(map(tuple, maze.get_nodes()))
        borders = [cell for cell in border_cells() if cell in accessible]
        start = random.choice(borders)
        end = random.choice([b for b in borders if b != start])
        return start, end

    def move(self, direction: str):
        direction = direction.upper()
        if direction not in DIRECTIONS:
            raise ValueError("Invalid direction. Use U, D, L, or R.")

        dr, dc = DIRECTIONS[direction]
        new_pos = (self.position_[0] + dr, self.position_[1] + dc)
        neighbors = set(map(tuple, self.maze.get_coord_neighbors(self.position_)))
        if new_pos in neighbors:
            self.position_ = new_pos
            self.path_.append(new_pos)
        else:
            print("Move blocked by wall.")

    def get_directions(self):
        neighbors = set(map(tuple, self.maze.get_coord_neighbors(self.position_)))
        allowed = []
        for d, (dr, dc) in DIRECTIONS.items():
            new_pos = (self.position_[0] + dr, self.position_[1] + dc)
            if new_pos in neighbors:
                allowed.append(d)
        return allowed

    def position(self):
        return self.position_

    def solved(self):
        return self.position_ == self.end

    def solve(self):
        self.maze = SolvedMaze.from_targeted_lattice_maze(self.maze)

    def print(self):
        if self.plot:
            MazePlot(self.maze).add_predicted_path(self.path_).plot()
            plt.show()
        else:
            ascii_maze = MazePlot(self.maze).add_predicted_path(self.path_).to_ascii()
            print(ascii_maze)

