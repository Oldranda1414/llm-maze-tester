from dataclasses import dataclass

from model import Model
from model.factory import random_model

@dataclass(frozen=True)
class ExperimentConfig:
    models: list[Model]
    maze_sizes: list[int]
    iterations: int
    provide_history: bool

def load_config() -> ExperimentConfig:
    models = [
        random_model('llama3')
    ]
    maze_sizes = [
        3, 4, 5, 6
    ]
    iterations = 10
    provide_history = True
    return ExperimentConfig(models, maze_sizes, iterations, provide_history)

