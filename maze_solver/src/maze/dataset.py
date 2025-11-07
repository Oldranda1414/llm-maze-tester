import random

from maze_dataset import MazeDataset as DatasetMazeDataset
from maze_dataset import MazeDatasetConfig
from maze_dataset.generation import LatticeMazeGenerators

from maze.lattice_maze import LatticeMaze
from maze import Maze

class MazeDataset():
    
    def __init__(self, name: str, n_mazes: int, maze_size: int, sight_depth: int, seed: int):
        random.seed(seed)
        config: MazeDatasetConfig = MazeDatasetConfig(
            name="dataset",
            grid_n=maze_size,
            n_mazes=n_mazes,
            maze_ctor=LatticeMazeGenerators.gen_dfs,
            seed=seed
        )

        dataset: MazeDataset = DatasetMazeDataset.from_config(config)

        save_path = f"{name}/maze"
        self.mazes: list[Maze] = [LatticeMaze(d_maze, sight_depth, f"{save_path}_{i}.png") for i, d_maze in enumerate(dataset.mazes)]
