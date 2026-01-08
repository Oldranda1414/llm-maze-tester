import statistics
from typing import Any, Callable

from run import Run
from util import seconds_to_padded_time


def mean_total_steps(runs: list[Run]):
    values = [len(r.chat_history.chat) for r in runs if r.is_solved]
    return "mean_total_steps (for solved)", statistics.mean(values)


def perc_solved(runs: list[Run]):
    solved = sum(r.is_solved for r in runs)
    return "perc_solved", solved / len(runs) * 100


def mean_execution_time(runs: list[Run]):
    mean_sec = statistics.mean(r.execution_time for r in runs if r.is_solved)
    return "mean_execution_time (for solved)", seconds_to_padded_time(mean_sec)


def mean_step_execution_time(runs: list[Run]):
    per_step = [
        r.execution_time / len(r.chat_history.chat)
        for r in runs
        if len(r.chat_history.chat) > 0 and r.is_solved
    ]
    mean_sec = statistics.mean(per_step)
    return "mean_step_execution_time (for solved)", seconds_to_padded_time(mean_sec)


STATS: list[Callable[[list[Run]], Any]] = [
    mean_total_steps,
    perc_solved,
    mean_execution_time,
    mean_step_execution_time,
]

# TODO
# mean_illegal_directions
# perc_illegal_directions
# mean_illegal_responses
# perc_illegal_responses
# mean_decisions
# total_execution_time
