from maze import Maze
from maze.dataset import MazeDataset

def create_dataset(n_mazes: int = 1, maze_size: int = 5, sight_depth: int = 2, seed: int = 42) -> MazeDataset:
    return MazeDataset("dataset", n_mazes, maze_size, sight_depth, seed)

def create_maze(size: int = 6, sight_depth: int = 2, seed: int = 42) -> Maze:
    return create_dataset(1, size, sight_depth, seed).mazes[0]

