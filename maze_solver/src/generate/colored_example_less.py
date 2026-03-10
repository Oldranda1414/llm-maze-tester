from maze.color.util import random_colored_cells
from maze.factory import create_maze


def colored_example_less(path: str):
    maze_size = 3
    n_colored_cells = 4
    colored_cells = random_colored_cells(1, maze_size, n_colored_cells)[0]
    maze = create_maze(maze_size, colored_cells=colored_cells)
    maze.save(f"{path}/colored_example_less.png", False, False, title="")
