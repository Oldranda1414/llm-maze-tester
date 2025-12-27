from maze.core.direction import Direction
from maze.factory import create_maze

def run() -> None:
    size = int(input("maze size?:"))
    maze = create_maze(seed=39, size=size)

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
            maze.save('./maze_test.png')
        else:
            maze.move(Direction.from_coordinate(move))

