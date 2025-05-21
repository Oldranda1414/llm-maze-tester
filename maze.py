import random
from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.plotting import MazePlot
import matplotlib.pyplot as plt

DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

class Maze:
    def __init__(self, width=6, height=6):
        self.width = width
        self.height = height
        self.maze = LatticeMazeGenerators.gen_dfs(
            grid_shape=(height, width),
            lattice_dim=2,
            accessible_cells=None,
            max_tree_depth=None,
            start_coord=None,
        )
        self.start, self.end = self._random_border_points()
        self.position_ = self.start

    def _random_border_points(self):
        def border_cells():
            return [
                (r, c)
                for r in range(self.height)
                for c in range(self.width)
                if r == 0 or r == self.height - 1 or c == 0 or c == self.width - 1
            ]

        accessible = set(map(tuple, self.maze.get_nodes()))
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

    def print(self):
        MazePlot(self.maze).plot()
        plt.show()

