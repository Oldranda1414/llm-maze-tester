"""entry point of the program
"""
import json

from maze_solver import MazeSolver

def main():
    """placeholder for real stuff
    """
    model_name = "llama3:latest"
    maze_width = 3
    maze_height = 3

    solved = False
    max_steps = 20
    min_steps = 5
    while not solved:
        history = []
        maze_solver = MazeSolver(model_name=model_name, maze_width=maze_width, maze_height=maze_height)
        step = 0
        while maze_solver.solved() is False and step < max_steps:
            try:
                step_history = maze_solver.step()
                history.append()
            except:
                print("exception occurred, restarting...")
                break
            step += 1
        if maze_solver.solved():
            print("maze solved!")
            if step > min_steps:
                solved = True
                print(maze_solver.get_statistics())
                save_history(history)
        else:
            print("maze not solved, retrying")

def save_history(history):
    with open('history.json', 'w') as file:
        json.dump(history, file)

if __name__ == "__main__":
    main()
