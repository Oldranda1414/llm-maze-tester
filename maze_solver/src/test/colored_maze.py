from maze.colored_cell import CellColor, ColoredCell
from maze.factory import create_maze


def run():
    colored_cells = [ColoredCell((0, 1), CellColor.BLACK)]
    create_maze(colored_cells=colored_cells)
