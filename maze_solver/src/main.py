import os
import logging
import time

from solver import MazeSolver

tab = "   "

def main():
    model_names = ["llama3"]
    maze_sizes = [3,4,5,6]
    iterations = 10

    for model_name in model_names:
        start_model = time.time()
        for maze_size in maze_sizes:
            start_size = time.time()
            for i in range(iterations):
                print(f"solving {maze_size}x{maze_size} maze with model {model_name} for {i} time")
                start_maze = time.time()
                max_steps = maze_size * maze_size * 10
                maze_solver = MazeSolver(model_name=model_name, maze_size=maze_size, quiet=True, seed=i)
                step = 0
                while not maze_solver.is_solved() and step < max_steps:
                    try:
                        maze_solver.step()
                    except Exception:
                        logging.error("Exception occurred", exc_info=True)
                    step += 1
                if maze_solver.is_solved():
                    print((tab * 3) + "maze solved!")
                else:
                    print((tab * 3) + "maze not solved...")
                print(maze_solver.get_statistics())
                print_time(3, f"maze {i}", start_maze)
                results_dir = f"results/{model_name}/{maze_size}x{maze_size}"
                os.makedirs(results_dir, exist_ok=True)
                maze_solver.save_run(f"{results_dir}/{i}.yaml")
            print_time(2, f"maze size {maze_size}", start_size)
        print_time(1, f"model {model_name}", start_model)

def print_time(indent: int, message: str, start_time: float):
    print((tab * indent) + f"Time taken for {message}: {time.time() - start_time:.2f} s")

if __name__ == "__main__":
    main()
