from maze.color.util import random_colored_cells
from maze.core.direction import Direction
from maze.factory import create_maze


def run():
    colored_cells = random_colored_cells(1, 6, 10)
    maze = create_maze(colored_cells=colored_cells[0], start=(1, 1))
    maze.move(Direction.WEST)
    maze.save("./test_colored_maze.png")
