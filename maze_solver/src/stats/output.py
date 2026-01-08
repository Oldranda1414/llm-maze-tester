from collections import defaultdict

from experiment import Experiment
from stats.types import StatFn


def print_experiment_stats(experiment: Experiment, stats: list[StatFn]) -> None:
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
        statistics = stat(runs)
        print(f"{statistics.name}: {statistics.value}")


def print_experiment_comparison(experiments: list[Experiment]) -> None:
    # TODO implement this
    _ = experiments
