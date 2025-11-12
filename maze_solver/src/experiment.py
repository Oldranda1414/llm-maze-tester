import os
import logging
import time

from solver import MazeSolver
from log import log
from util import seconds_to_padded_time

tab = "   "

class Experiment:
    def __init__(self, model_names: list[str], maze_sizes: list[int], iterations: int):
        self.model_names = model_names
        self.maze_sizes = maze_sizes
        self.iterations = iterations

    def run(self):
        for model_name in self.model_names:
            start_model = time.time()
            for maze_size in self.maze_sizes:
                start_size = time.time()
                for i in range(self.iterations):
                    solved_mazes = 0
                    log(f"solving {maze_size}x{maze_size} maze with model {model_name} for {i} time")
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
                        log((tab * 3) + "maze solved!")
                        solved_mazes += 1
                    else:
                        log((tab * 3) + "maze not solved...")
                    log(str(maze_solver.get_statistics()))
                    log_time(3, f"maze {i}", start_maze)
                    results_dir = f"results/{model_name}/{maze_size}x{maze_size}"
                    os.makedirs(results_dir, exist_ok=True)
                    maze_solver.save_run(f"{results_dir}/{i}.yaml", delta_t(start_maze))
                log_time(2, f"maze size {maze_size}", start_size)
                log("solved mazes / attempted mazes: {solved_mazes}/{iterations}")
            log_time(1, f"model {model_name}", start_model)

def log_time(indent: int, message: str, start_time: float):
    log((tab * indent) + f"Time taken for {message}: {seconds_to_padded_time(delta_t(start_time))}")

def delta_t(start_time: float) -> float:
    return time.time() - start_time
