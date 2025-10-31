from maze import Maze
from maze.lattice_maze import LatticeMaze

def create_maze(size: int = 6, save_path: str = "maze.png") -> Maze:
    return LatticeMaze(size, save_path)
