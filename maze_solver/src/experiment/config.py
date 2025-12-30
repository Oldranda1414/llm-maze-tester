from dataclasses import dataclass

from model import Model
from model.factory import random_model
from prompt import PromptGenerator
from prompt.style.empty import EmptyStyle

@dataclass(frozen=True)
class ExperimentConfig:
    models: list[Model]
    prompt_generator: PromptGenerator
    maze_sizes: list[int]
    iterations: int
    provide_history: bool
    quiet: bool

def load_config() -> ExperimentConfig:
    models = [
        random_model('llama3')
    ]
    prompt_generator = PromptGenerator(EmptyStyle())
    maze_sizes = [
        3, 4, 5, 6
    ]
    iterations = 10
    provide_history = True
    quiet = True
    return ExperimentConfig(models, prompt_generator, maze_sizes, iterations, provide_history, quiet)

