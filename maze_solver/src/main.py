import os
from solver import MazeSolver
from llm.model import model_names
import time

def main():
    for model_name in model_names:
        results_path = f"results/{model_name}"
        os.makedirs(results_path, exist_ok=True)
        start_model = time.time()
        for maze_size in [3,4,5,6]:
            start_size = time.time()
            for i in range(20):
                #print(f"solving {maze_size}x{maze_size} maze with model {model_name} for {i} time")
                start_maze = time.time()
                max_steps = maze_size * maze_size * 10
                maze_solver = MazeSolver(model_name=model_name, maze_size=maze_size, quiet=True, seed=i)
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
                #print(maze_solver.get_statistics())
                print_time(3, f"maze {i}", start_maze)
                maze_solver.save_run(f"{results_path}/{maze_size}x{maze_size}/{i}.yaml")
            print_time(2, f"maze size {maze_size}", start_size)
        print_time(1, f"model {model_name}", start_model)

def print_time(indent: int, message: str, start_time: float):
    print(("   " * indent) + f"Time taken for {message}: {time.time() - start_time:.2f} s")

if __name__ == "__main__":
    main()
