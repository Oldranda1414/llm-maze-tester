from collections import defaultdict
from typing import Callable

from experiment import Experiment
from stats.types import StatFn


def print_experiment_stats(
    experiment: Experiment,
    stats: list[StatFn],
    print_fn: Callable[[str], None] = print,
    print_overall: bool = True,
) -> None:
    if not experiment.runs:
        print_fn("No runs provided.")
        return

    for model, runs in experiment.runs.items():
        print_fn(f"\n===== Model: {model} =====")

        runs_by_size = defaultdict(list)
        for run in runs:
            runs_by_size[run.maze_size].append(run)

        for size, size_runs in sorted(runs_by_size.items()):
            print_fn(f"\n=== Maze size: {size} ===")
            print_stats(size_runs, stats, print_fn)

        if print_overall:
            print_fn("\n=== Overall stats ===")
            print_stats(runs, stats, print_fn)


def print_stats(runs: list, stats: list[StatFn], print_fn: Callable[[str], None]):
    for stat in stats:
        statistics = stat(runs)
        print_fn(f"{statistics.name}: {statistics.value}")
