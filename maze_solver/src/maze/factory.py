
from maze import Maze, generate_start, generate_target
from maze.dataset import MazeDataset
from maze.lattice_maze import LatticeMaze
from move import Coordinate

def create_dataset(n_mazes: int = 1, maze_size: int = 5, sight_depth: int = 2, seed: int = 42) -> MazeDataset:
    return MazeDataset("dataset", n_mazes, maze_size, sight_depth, seed)

def create_maze(size: int = 6, start: Coordinate | None = None, target: Coordinate | None = None, sight_depth: int = 2, seed: int = 42) -> Maze:
    random_maze = create_dataset(1, size, sight_depth, seed).mazes[0]
    if target is None:
        target = generate_target(size)
    if start is None:
        start = generate_start(size, target)
    return LatticeMaze(random_maze.connection_list(), size, start, target, sight_depth)

