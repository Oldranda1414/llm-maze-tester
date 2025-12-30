import os
import logging
import time
from datetime import datetime
from collections import defaultdict
import statistics

from util import seconds_to_padded_time
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

    def print_experiment_stats(self):
        """
        Computes and prints statistics on a list of Run objects.
        Statistics are grouped by maze size and also shown overall.
        """
        if not self.runs:
            print("No runs provided.")
            return

        # Organize runs by maze size
        runs_by_size = defaultdict(list)
        for run in self.runs:
            size = run.maze_size
            runs_by_size[size].append(run)

        # Print stats per maze size
        for size, run_list in sorted(runs_by_size.items()):
            stats = compute_stats(run_list)
            print(f"\n=== Maze size: {size} ===")
            for k, v in stats.items():
                if type(v) == float:
                    v = f"{v:.2f}"
                print(f"{k}: {v}")

        # Compute overall stats
        overall_stats = compute_stats(self.runs)
        print(f"\n=== Overall stats ===")
        for k, v in overall_stats.items():
            if type(v) == float:
                v = f"{v:.2f}"
            print(f"{k}: {v}")

def compute_stats(run_list):
    total_steps_list = [len(r.chat_history.chat) for r in run_list]
    illegal_dirs_list = [r.illegal_directions for r in run_list]
    illegal_resps_list = [r.illegal_responses for r in run_list]
    decisions_list = [len(r.maze.decisions) for r in run_list]
    execution_list = [r.execution_time for r in run_list]
    solved_list = [r.is_solved for r in run_list]

    step_execution_times = [
        exec_t / steps
        for exec_t, steps in zip(execution_list, total_steps_list)
        if steps > 0
    ]
    mean_step_execution_seconds = statistics.mean(step_execution_times)
    mean_step_execution_time = seconds_to_padded_time(mean_step_execution_seconds)

    mean_illegal_dirs = statistics.mean(illegal_dirs_list)
    perc_illegal_dirs = statistics.mean([
        id_ / ts * 100 if ts > 0 else 0
        for id_, ts in zip(illegal_dirs_list, total_steps_list)
    ])

    mean_illegal_resps = statistics.mean(illegal_resps_list)
    perc_illegal_resps = statistics.mean([
        ir / ts * 100 if ts > 0 else 0
        for ir, ts in zip(illegal_resps_list, total_steps_list)
    ])

    mean_total_steps = statistics.mean(total_steps_list)
    mean_decisions = statistics.mean(decisions_list)
    perc_solved = sum(solved_list) / len(solved_list) * 100

    mean_execution = seconds_to_padded_time(statistics.mean(execution_list))
    total_execution = seconds_to_padded_time(sum(execution_list))

    return {
        "mean_illegal_directions": mean_illegal_dirs,
        "perc_illegal_directions": perc_illegal_dirs,
        "mean_illegal_responses": mean_illegal_resps,
        "perc_illegal_responses": perc_illegal_resps,
        "mean_total_steps": mean_total_steps,
        "mean_decisions": mean_decisions,
        "perc_solved": perc_solved,
        "mean_execution_time": mean_execution,
        "total_execution_time": total_execution,
        "mean_step_execution_time": mean_step_execution_time,
    }

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
                model.reset_history()
                maze_solver = MazeSolver(model, config.prompt_generator, mazes[i], quiet=config.quiet)
                step = 0
                while not maze_solver.is_solved() and step < max_steps:
                    try:
                        maze_solver.step(config.provide_history)
                    except Exception:
                        logging.error("Exception occurred", exc_info=True)
                    step += 1
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

