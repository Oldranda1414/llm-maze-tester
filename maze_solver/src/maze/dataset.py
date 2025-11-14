import random

from maze_dataset import MazeDataset as DatasetMazeDataset, MazeDatasetConfig
from maze_dataset.generation import LatticeMazeGenerators

from maze import Maze, generate_start, generate_target
from maze.core.connection_list import ConnectionList
from maze.lattice_maze import LatticeMaze

class MazeDataset():
    
    def __init__(self, name: str, n_mazes: int, maze_size: int, sight_depth: int, seed: int):
        random.seed(seed)
        config: MazeDatasetConfig = MazeDatasetConfig(
            name=name,
            grid_n=maze_size,
            n_mazes=n_mazes,
            maze_ctor=LatticeMazeGenerators.gen_dfs,
            seed=seed
        )

        dataset: DatasetMazeDataset = DatasetMazeDataset.from_config(config)

        target = generate_target(maze_size)
        start = generate_start(maze_size, target)
        self.mazes: list[Maze] = [
                LatticeMaze(
                    ConnectionList(d_maze.connection_list[0].tolist(), d_maze.connection_list[1].tolist()),
                    maze_size,
                    start,
                    target,
                    sight_depth)
                for d_maze in dataset.mazes
            ]
