import os
import time
from datetime import datetime
import logging

from maze.factory import create_dataset
from model import Model
from solver import MazeSolver
from experiment.utils import delta_t, log_time, tab

from experiment.config import ExperimentConfig
from experiment.log import log


def run_experiment(config: ExperimentConfig):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    for model in config.models:
        if config.mazes is None:
            run_generated_mazes(model, config, timestamp)
        else:
            run_custom_mazes(model, config, timestamp)


def run_custom_mazes(model: Model, config: ExperimentConfig, timestamp: str):
    if config.mazes is None:
        raise ValueError(
            "run_custom_mazes was called with ExperimentConfig.mazes == None\n"
            "run_custom_mazes must be called with ExperimentConfig.mazes == list[Maze]"
        )

    start = time.time()
    mazes = list(config.mazes)
    results_dir = f"results/{timestamp}/{model.name}/custom"

    run_maze_batch(
        model=model,
        mazes=mazes,
        config=config,
        results_dir=results_dir,
    )

    log_time(1, f"model {model.name}", start)


def run_generated_mazes(model: Model, config: ExperimentConfig, timestamp: str):
    start_model = time.time()

    for maze_size in config.maze_sizes:
        start_size = time.time()

        dataset = create_dataset(config.iterations, maze_size)
        results_dir = f"results/{timestamp}/{model.name}/{maze_size}x{maze_size}"

        run_maze_batch(
            model=model,
            mazes=dataset.mazes,
            config=config,
            results_dir=results_dir,
        )

        log_time(2, f"maze size {maze_size}", start_size)

    log_time(1, f"model {model.name}", start_model)


def run_maze_batch(
    *,
    model: Model,
    mazes: list,
    config: ExperimentConfig,
    results_dir: str,
):
    solved = 0

    for i, maze in enumerate(mazes):
        if solve_single_maze(
            model=model,
            maze=maze,
            prompt_generator=config.prompt_generator,
            provide_history=config.provide_history,
            quiet=config.quiet,
            results_dir=results_dir,
            run_id=i,
        ):
            solved += 1

    log(f"solved mazes / attempted mazes: {solved}/{len(mazes)}")


def solve_single_maze(
    *,
    model: Model,
    maze,
    prompt_generator,
    provide_history: bool,
    quiet: bool,
    results_dir: str,
    run_id: int,
) -> bool:
    maze_size = maze.size
    max_steps = maze_size * maze_size * 10

    log(f"solving {maze_size}x{maze_size} maze with model {model.name}")
    start = time.time()

    solver = MazeSolver(
        model=model,
        prompt_generator=prompt_generator,
        maze=maze,
        quiet=quiet,
    )

    steps = 0
    while not solver.is_solved() and steps < max_steps:
        try:
            solver.step(provide_history)
            steps += 1
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            break

    if solver.is_solved():
        log((tab * 3) + "maze solved!")
        solved = True
    else:
        log((tab * 3) + "maze not solved...")
        solved = False

    os.makedirs(results_dir, exist_ok=True)
    solver.save_run(f"{results_dir}/{run_id}.yaml", delta_t(start))
    log_time(3, f"maze {run_id}", start)

    return solved
