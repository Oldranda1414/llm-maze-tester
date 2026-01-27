from dataclasses import dataclass

from maze import Maze

from maze.color.util import random_colored_cells
from model import Model
from model.factory import llm_model

from prompt import PromptGenerator
from prompt.config import PromptConfig

from maze.factory import create_dataset
from prompt.style.narrative import NarrativeStyle
from solver import PreambleLocation


@dataclass(frozen=True)
class ExperimentConfig:
    models: list[Model]
    prompt_generator: PromptGenerator
    preamble_location: PreambleLocation
    maze_sizes: list[int]
    iterations: int
    provide_history: bool
    quiet: bool
    mazes: list[Maze] | None = None


def load_config() -> ExperimentConfig:
    models = [
        llm_model("deepseek-r1:32b"),
    ]
    prompt_config = PromptConfig(
        provide_legal_output_hint=True,
        provide_spacial_awerness_hint=False,
        provide_color_hint=True,
        provide_repetition_hint=True,
        provide_steps_summary=0,
        provide_possible_moves=False,
    )
    prompt_style = NarrativeStyle()
    maze_sizes = [3]
    iterations = 10
    provide_history = True
    quiet = True
    return ExperimentConfig(
        models=models,
        prompt_generator=PromptGenerator(prompt_style, prompt_config),
        preamble_location=PreambleLocation.SYSTEM,
        maze_sizes=maze_sizes,
        iterations=iterations,
        provide_history=provide_history,
        quiet=quiet,
        mazes=_hard_3x3_mazes(),
    )


def _hard_3x3_mazes():
    colored_cells_number = 5
    colored_cells = random_colored_cells(1, 3, colored_cells_number)[0]
    mazes = create_dataset(10, 3, colored_cells=[colored_cells] * 10).mazes
    indexes = [4]
    return [maze for i, maze in enumerate(mazes) if i in indexes]
