from move import Direction
from maze.factory import create_maze

if __name__ == "__main__":
    maze = create_maze(seed=39)

    print("Start:", maze.start())
    print("End:", maze.target())
    print("Initial position:", maze.position())

    while not maze.solved():
        maze.print()

        print("Available directions:", maze.get_directions())

        prompt = "give me a move (C to close, S to save): "
        move = input(prompt)
        move = move.strip(" ").upper()
        coordinates = ["N", "E", "S", "W"]
        actions = ["C", "S"]
        while move not in coordinates + actions:
            print("invalid move try again")
            move = input(prompt)

        if move == "C":
            break
        if move == "S":
            maze.save('./maze_test.png')

        maze.move(Direction.from_coordinate(move))
        print("New position:", maze.position())
        print("Solved?", maze.solved())

