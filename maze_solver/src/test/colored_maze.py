from maze.colored_cell import CellColor, ColoredCell, random_colored_cells
from maze.core.direction import Direction
from maze.factory import create_maze


def run():
    # colored_cells = [ColoredCell((1, 1), CellColor.ORANGE)]
    colored_cells = random_colored_cells(1, 6, 10)
    maze = create_maze(colored_cells=colored_cells[0], start=(1, 1))
    maze.move(Direction.WEST)
    maze.save("./test_colored_maze.png")
