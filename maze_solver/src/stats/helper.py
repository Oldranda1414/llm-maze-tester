from statistics import mean
from typing import Callable, Iterable

from stats.types import Statistic
from util import format_float


def mean_stat(
    name: str,
    values: Iterable[float | int],
    formatter: Callable[[float], str] = format_float,
) -> Statistic:
    values = list(values)
    if not values:
        return Statistic(name, "N/A")
    return Statistic(name, formatter(mean(values)))
