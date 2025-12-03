from typing import Callable
import random

from maze import Maze, generate_start, generate_target
from maze.dataset import MazeDataset
from maze.lattice_maze import LatticeMaze
from maze.core.coordinate import Coordinate

def _is_non_trivial(maze: Maze) -> bool:
    alpha = 0.25
    size = maze.size
    min_path_lenght = round(size * size * alpha)
    return len(maze.solution) >= min_path_lenght

def create_dataset(n_mazes: int = 1, maze_size: int = 5, sight_depth: int = 2, seed: int = 42, maze_filter: Callable[[Maze], bool] | None = _is_non_trivial) -> MazeDataset:
    return MazeDataset("dataset", n_mazes, maze_size, sight_depth, seed, maze_filter)

def create_maze(size: int = 6, start: Coordinate | None = None, target: Coordinate | None = None, sight_depth: int = 2, seed: int = 42, maze_filter: Callable[[Maze], bool] | None = _is_non_trivial) -> Maze:
    rng = random.Random(seed)
    random_maze = create_dataset(1, size, sight_depth, seed, maze_filter).mazes[0]
    if target is None:
        target = generate_target(size, rng)
    if start is None:
        start = generate_start(size, target, rng)
    return LatticeMaze(random_maze.connection_list, size, start, target, sight_depth)

def maze_from_yaml(yaml_str: str) -> Maze:
    return LatticeMaze.from_yaml(yaml_str)
