from typing import Callable

from run import Run
from stats.helper import mean_stat
from util import seconds_to_padded_time, format_float
from stats.types import Statistic


def mean_illegal_directions(runs: list[Run]) -> Statistic:
    name = "mean illegal directions"
    values = [r.illegal_directions for r in runs]
    return mean_stat(name, values)


def perc_illegal_directions(runs: list[Run]) -> Statistic:
    name = "perc illegal directions"
    illegal_dirs = [r.illegal_directions for r in runs]
    total_steps = [len(r.chat_history.chat) for r in runs]
    values = [
        illegal / steps * 100 if steps > 0 else 0
        for illegal, steps in zip(illegal_dirs, total_steps)
    ]
    return mean_stat(name, values)


def mean_illegal_responses(runs: list[Run]) -> Statistic:
    name = "mean illegal responses"
    values = [r.illegal_responses for r in runs]
    return mean_stat(name, values)


def perc_illegal_responses(runs: list[Run]) -> Statistic:
    name = "perc illegal responses"
    illegal_responses = [r.illegal_responses for r in runs]
    total_steps = [len(r.chat_history.chat) for r in runs]

    values = [
        ir / ts * 100 if ts > 0 else 0 for ir, ts in zip(illegal_responses, total_steps)
    ]
    return mean_stat(name, values)


def mean_total_steps(runs: list[Run]) -> Statistic:
    name = "mean total steps (for solved)"
    values = [len(r.chat_history.chat) for r in runs if r.is_solved]
    return mean_stat(name, values)


def mean_decisions(runs: list[Run]) -> Statistic:
    name = "mean decisions (for solved)"
    print(runs[0].maze.decisions)
    values = [len(r.maze.decisions) for r in runs if r.is_solved]
    return mean_stat(name, values)


def perc_solved(runs: list[Run]) -> Statistic:
    name = "perc solved"
    solved = sum(r.is_solved for r in runs)
    return Statistic(name, format_float(solved / len(runs) * 100))


def mean_execution_time(runs: list[Run]) -> Statistic:
    name = "mean execution time (for solved)"
    values = [r.execution_time for r in runs if r.is_solved]
    return mean_stat(name, values, seconds_to_padded_time)


def mean_step_execution_time(runs: list[Run]) -> Statistic:
    name = "mean step execution time (for solved)"
    values = [
        r.execution_time / len(r.chat_history.chat)
        for r in runs
        if len(r.chat_history.chat) > 0 and r.is_solved
    ]
    return mean_stat(name, values, seconds_to_padded_time)


def total_execution_time(runs: list[Run]) -> Statistic:
    name = "total execution time"
    execution_times = [r.execution_time for r in runs]
    return Statistic(name, seconds_to_padded_time(sum(execution_times)))


STATS: list[Callable[[list[Run]], Statistic]] = [
    mean_illegal_directions,
    perc_illegal_directions,
    mean_illegal_responses,
    perc_illegal_responses,
    mean_total_steps,
    mean_decisions,
    perc_solved,
    mean_execution_time,
    mean_step_execution_time,
    total_execution_time,
]
