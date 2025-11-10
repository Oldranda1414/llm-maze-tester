"""entry point of the program
"""
import os
from solver import MazeSolver
from llm.model import model_names

def main():
    """placeholder for real stuff
    """
    for model_name in model_names:
        results_path = f"results/{model_name}"
        os.makedirs(results_path, exist_ok=True)
        for maze_size in [2,3,4,5]:
            solved = False
            max_steps = maze_size * maze_size
            while not solved:
                maze_solver = MazeSolver(model_name=model_name, maze_size=maze_size)
                step = 0
                while not maze_solver.solved() and step < max_steps:
                    try:
                        maze_solver.step()
                        step += 1
                    except:
                        print("exception occurred...")
                        break
                if maze_solver.solved():
                    print("maze solved!")
                else:
                    print("maze not solved...")
                maze_solver.save_run(f"{results_path}/{maze_size}.yaml")

if __name__ == "__main__":
    main()
