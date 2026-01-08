from collections import defaultdict
from typing import Any, Callable

from experiment import Experiment

StatFn = Callable[[list], tuple[str, Any]]


def print_experiment_stats(experiment: Experiment, stats: list[StatFn]):
    if not experiment.runs:
        print("No runs provided.")
        return

    runs_by_size = defaultdict(list)
    for run in experiment.runs:
        runs_by_size[run.maze_size].append(run)

    for size, runs in sorted(runs_by_size.items()):
        print(f"\n=== Maze size: {size} ===")
        print_stats(runs, stats)

    print("\n=== Overall stats ===")
    print_stats(experiment.runs, stats)


def print_stats(runs: list, stats: list[StatFn]):
    for stat in stats:
        name, value = stat(runs)
        if isinstance(value, float):
            value = f"{value:.2f}"
        print(f"{name}: {value}")
