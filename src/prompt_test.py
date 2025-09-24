from maze import Maze
from prompt import generate_prompt

def main():
    maze = Maze(block_on_plot=False, plot=False)

    while not maze.solved():

        maze.print()

        print("Available directions:", maze.get_directions())
        print("generated prompt:")
        print(generate_prompt(maze))

        move = input("give me a move (C to close): ")
        move = move.strip(" ").upper()
        while move not in ["U","D","L","R", "C"]:
            print("invalid move try again")
            move = input("give me a move (C to close): ")

        if move == "C":
            break

        maze.move(move)
        print("New position:", maze.position())
        print("Solved?", maze.solved())

    input("press any button to exit")

if __name__ == "__main__":
    main()
