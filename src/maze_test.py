from maze import Maze
from move import Direction

if __name__ == "__main__":
    maze = Maze()

    print("Start:", maze.start)
    print("End:", maze.end)
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

    input("press any button to exit")

