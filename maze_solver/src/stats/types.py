from dataclasses import dataclass
from typing import Callable


@dataclass()
class Statistic:
    name: str
    value: str


StatFn = Callable[[list], Statistic]
