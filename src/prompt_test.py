from maze import Maze, Direction
from prompt import generate_step_prompt, preamble

def main():
    maze = Maze(3, 3)
    print(preamble(maze))

    while not maze.solved():

        # print("Available directions:", [direction.to_coordinate() for direction in maze.get_directions()])
        # print("generated prompt:")
        print(generate_step_prompt(maze))
        maze.print()

        move = input("give me a move (C to close): ")
        move = move.strip(" ").upper()
        while move not in ["N", "E", "S", "W", "C"]:
            print("invalid move try again")
            move = input("give me a move (C to close): ")
            move = move.strip(" ").upper()

        if move == "C":
            break

        maze.move(Direction.from_coordinate(move))
        print("New position:", maze.position())
        print("Solved?", maze.solved())

    input("press any button to exit")

if __name__ == "__main__":
    main()
