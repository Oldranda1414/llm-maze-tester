from dataclasses import dataclass

from model import Model
from model.factory import llm_model
from prompt import PromptGenerator
from prompt.style.narrative import NarrativeStyle

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
        llm_model('deepseek-r1')
    ]
    prompt_generator = PromptGenerator(NarrativeStyle())
    maze_sizes = [
        3, 4, 5, 6
    ]
    iterations = 10
    provide_history = True
    quiet = True
    return ExperimentConfig(models, prompt_generator, maze_sizes, iterations, provide_history, quiet)

