from maze.color.util import random_colored_cells
from maze.factory import create_maze


def colored_example(path: str):
    maze_size = 3
    n_colored_cells = 6
    colored_cells = random_colored_cells(1, maze_size, n_colored_cells)[0]
    maze = create_maze(maze_size, colored_cells=colored_cells)
    maze.save(f"{path}/colored_example.png", False, False)
