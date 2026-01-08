import os
import logging
import time
from datetime import datetime

from run import Run

from experiment.config import ExperimentConfig
from experiment.utils import delta_t, log_time, tab
from experiment.log import log

from maze.factory import create_dataset
from solver import MazeSolver

class Experiment:
    def __init__(self, date: str):
        base_path = "results"
        experiment_path = os.path.join(base_path, date)
        self.runs: list[Run] = []

        # Walk through all subdirectories and find YAML files
        for root, _, files in os.walk(experiment_path):
            for file in files:
                if file.endswith(".yaml"):
                    file_path = os.path.join(root, file)
                    run = Run.load(file_path)
                    self.runs.append(run)

def run_experiment(config: ExperimentConfig):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    for model in config.models:
        start_model = time.time()
        for maze_size in config.maze_sizes:
            start_size = time.time()
            results_dir = f"results/{timestamp}/{model.name}/{maze_size}x{maze_size}"
            mazes = create_dataset(config.iterations, maze_size).mazes
            solved_mazes = 0
            for i in range(config.iterations):
                log(f"solving {maze_size}x{maze_size} maze with model {model.name} for {i} time")
                start_maze = time.time()
                max_steps = maze_size * maze_size * 10
                maze_solver = MazeSolver(model, config.prompt_generator, mazes[i], quiet=config.quiet)
                step = 0
                while not maze_solver.is_solved() and step < max_steps:
                    try:
                        maze_solver.step(config.provide_history)
                        step += 1
                    except Exception:
                        logging.error("Exception occurred", exc_info=True)
                        break
                if maze_solver.is_solved():
                    log((tab * 3) + "maze solved!")
                    solved_mazes += 1
                else:
                    log((tab * 3) + "maze not solved...")
                log_time(3, f"maze {i}", start_maze)
                os.makedirs(results_dir, exist_ok=True)
                maze_solver.save_run(f"{results_dir}/{i}.yaml", delta_t(start_maze))
            log_time(2, f"maze size {maze_size}", start_size)
            log(f"solved mazes / attempted mazes: {solved_mazes}/{config.iterations}")
        log_time(1, f"model {model.name}", start_model)


def experiment_list():
    experiments = [d for d in os.listdir('results') if os.path.isdir(os.path.join('results', d))]
    experiments.remove("logs")
    experiments.sort()
    return experiments if experiments else []

