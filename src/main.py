"""entry point of the program
"""

from maze_solver import MazeSolver

def main():
    """placeholder for real stuff
    """
    model_name = "llama3:latest"
    maze_width = 3
    maze_height = 3

    solved = False
    max_steps = 20
    while not solved:
        maze_solver = MazeSolver(model_name=model_name, maze_width=maze_width, maze_height=maze_height)
        step = 0
        while maze_solver.solved() is False and step < max_steps:
            try:
                maze_solver.step()
            except:
                print("exception occurred, restarting...")
                break
            step += 1
        if maze_solver.solved():
            print("maze solved!")
            solved = True
        else:
            print("maze not solved, retrying")

if __name__ == "__main__":
    main()
