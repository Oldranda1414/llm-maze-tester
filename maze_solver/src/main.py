"""entry point of the program
"""
import os
from solver import MazeSolver
from llm.model import model_names
import time

def main():
    """placeholder for real stuff
    """
    for model_name in model_names:
        results_path = f"results/{model_name}"
        os.makedirs(results_path, exist_ok=True)
        for maze_size in [2,3,4,5]:
            print(f"solving {maze_size}x{maze_size} maze with model {model_name}")
            start = time.time()
            max_steps = maze_size * 10
            maze_solver = MazeSolver(model_name=model_name, maze_size=maze_size, quiet=True)
            step = 0
            while not maze_solver.solved() and step < max_steps:
                try:
                    maze_solver.step()
                except Exception as e:
                    print("exception occurred...")
                    #raise e
                step += 1
            if maze_solver.solved():
                print("maze solved!")
            else:
                print("maze not solved...")
            print(maze_solver.get_statistics())
            print(f"Time taken: {time.time() - start:.2f} s")
            maze_solver.save_run(f"{results_path}/{maze_size}.yaml")

if __name__ == "__main__":
    main()
