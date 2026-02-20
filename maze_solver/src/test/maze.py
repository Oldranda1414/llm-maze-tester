from maze.color.util import random_colored_cells
from maze.core.direction import Direction
from maze.factory import create_maze


def run() -> None:
    size = int(input("maze size?:"))
    tile_number = int(input("tile number?:"))
    maze = create_maze(
        size=size, colored_cells=random_colored_cells(1, 3, tile_number)[0]
    )

    print("Start:", maze.start)
    print("End:", maze.target)
    print("Initial position:", maze.position)

    while not maze.solved:
        maze.print()

        print("Available directions:", maze.available_directions())

        prompt = "give me a move (C to close, Q to save): "
        move = input(prompt)
        move = move.strip(" ").upper()
        coordinates = ["N", "E", "S", "W"]
        actions = ["C", "Q"]
        while move not in coordinates + actions:
            print("invalid move try again")
            move = input(prompt)

        if move == "C":
            break
        elif move == "Q":
            maze.save("./maze_test.png", draw_character=False)
        else:
            maze.move(Direction.from_coordinate(move))
