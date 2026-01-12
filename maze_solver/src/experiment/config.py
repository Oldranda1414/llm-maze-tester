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
        llm_model("llama3"),
        llm_model("qwen3"),
        llm_model("smollm2"),
        llm_model("phi4-mini"),
        llm_model("deepseek-r1"),
        llm_model("mistral"),
    ]
    prompt_config = PromptConfig(
        provide_steps_summary=None, provide_possible_moves=False
    )
    prompt_style = NarrativeStyle()
    maze_sizes = [3]
    iterations = 10
    provide_history = True
    quiet = True
    return ExperimentConfig(
        models=models,
        prompt_generator=PromptGenerator(prompt_style, prompt_config),
        maze_sizes=maze_sizes,
        iterations=iterations,
        provide_history=provide_history,
        quiet=quiet,
    )
