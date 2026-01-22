from dataclasses import dataclass

from maze import Maze
from maze.factory import create_dataset

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
    mazes: list[Maze] | None = None


def load_config() -> ExperimentConfig:
    models = [
        llm_model("glm-4.7-flash"),
        llm_model("yi"),
    ]
    prompt_config = PromptConfig(provide_steps_summary=0, provide_possible_moves=False)
    prompt_style = NarrativeStyle()
    maze_sizes = [3, 4]
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
        mazes=None,
    )


def hard_3x3_mazes():
    mazes = create_dataset(10, 3).mazes
    indexes = [4]
    return [maze for i, maze in enumerate(mazes) if i in indexes]
