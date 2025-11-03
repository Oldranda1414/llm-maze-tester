from move import Direction
from prompt import generate_step_prompt, preamble
from maze.factory import create_maze, create_dataset

def main():
    maze = create_maze(3)
    print(preamble(maze))

    while not maze.solved():

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

def many_maze():
    mazes = create_dataset(10,3).mazes
    for maze in mazes:
        print(preamble(maze))

        while not maze.solved():

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

if __name__ == "__main__":
    main()
