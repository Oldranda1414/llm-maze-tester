from dataclasses import dataclass

from model import Model
from model.factory import llm_model
from prompt import PromptGenerator
from prompt.config import PromptConfig
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
    prompt_config = PromptConfig(provide_steps_summary=False, provide_possible_moves=False)
    prompt_style = NarrativeStyle()
    maze_sizes = [
        3
    ]
    iterations = 10
    provide_history = True
    quiet = True
    return ExperimentConfig(models, PromptGenerator(prompt_style, prompt_config), maze_sizes, iterations, provide_history, quiet)

