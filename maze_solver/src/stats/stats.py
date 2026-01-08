from statistics import mean
from typing import Callable

from run import Run
from util import seconds_to_padded_time, format_float
from stats.types import Statistic


def mean_illegal_directions(runs: list[Run]) -> Statistic:
    values = [r.illegal_directions for r in runs]
    return Statistic("mean illegal directions", format_float(mean(values)))


def perc_illegal_directions(runs: list[Run]) -> Statistic:
    illegal_dirs = [r.illegal_directions for r in runs]
    total_steps = [len(r.chat_history.chat) for r in runs]

    result = mean(
        [id / ts * 100 if ts > 0 else 0 for id, ts in zip(illegal_dirs, total_steps)]
    )
    return Statistic("perc illegal directions", format_float(result))


def mean_illegal_responses(runs: list[Run]) -> Statistic:
    values = [r.illegal_responses for r in runs]
    return Statistic("mean illegal responses", format_float(mean(values)))


def perc_illegal_responses(runs: list[Run]) -> Statistic:
    illegal_responses = [r.illegal_responses for r in runs]
    total_steps = [len(r.chat_history.chat) for r in runs]

    result = mean(
        [
            ir / ts * 100 if ts > 0 else 0
            for ir, ts in zip(illegal_responses, total_steps)
        ]
    )
    return Statistic("perc illegal responses", format_float(result))


def mean_total_steps(runs: list[Run]) -> Statistic:
    name = "mean total steps (for solved)"
    values = [len(r.chat_history.chat) for r in runs if r.is_solved]
    if len(values) == 0:
        return Statistic(name, "N/A")
    return Statistic(name, format_float(mean(values)))


def mean_decisions(runs: list[Run]) -> Statistic:
    name = "mean decisions (for solved)"
    values = [len(r.maze.decisions) for r in runs if r.is_solved]
    if len(values) == 0:
        return Statistic(name, "N/A")
    return Statistic(name, format_float(mean(values)))


def perc_solved(runs: list[Run]) -> Statistic:
    solved = sum(r.is_solved for r in runs)
    return Statistic("perc solved", format_float(solved / len(runs) * 100))


def mean_execution_time(runs: list[Run]) -> Statistic:
    name = "mean execution time (for solved)"
    values = [r.execution_time for r in runs if r.is_solved]
    if len(values) == 0:
        return Statistic(name, "N/A")
    return Statistic(name, seconds_to_padded_time(mean(values)))


def mean_step_execution_time(runs: list[Run]) -> Statistic:
    name = "mean step execution time (for solved)"
    per_step = [
        r.execution_time / len(r.chat_history.chat)
        for r in runs
        if len(r.chat_history.chat) > 0 and r.is_solved
    ]
    if len(per_step) == 0:
        return Statistic(name, "N/A")
    mean_sec = mean(per_step)
    return Statistic(name, seconds_to_padded_time(mean_sec))


def total_execution_time(runs: list[Run]) -> Statistic:
    execution_times = [r.execution_time for r in runs]
    return Statistic(
        "total execution time", seconds_to_padded_time(sum(execution_times))
    )


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
