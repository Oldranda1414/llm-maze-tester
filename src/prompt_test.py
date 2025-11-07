from move import Direction
from prompt import step_prompt, get_preamble
from maze.factory import create_maze, create_dataset

def main():
    sight_depth = 3
    maze = create_maze(3, sight_depth)
    print(get_preamble(maze))

    while not maze.solved():

        print(step_prompt(maze))
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
    sight_depth = 3
    mazes = create_dataset(10,3, sight_depth).mazes
    for maze in mazes:
        print(get_preamble(maze))

        while not maze.solved():

            print(step_prompt(maze))
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

