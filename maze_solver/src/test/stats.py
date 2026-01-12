from experiment import Experiment
from stats.stats import mean_decisions


def run():
    runs = Experiment("2026-01-11_12:48:24").runs
    for run in runs:
        print(run.maze.decisions)
    stat = mean_decisions(runs)
    print(stat)
