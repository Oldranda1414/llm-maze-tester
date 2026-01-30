from dataclasses import dataclass
from typing import Callable
from copy import deepcopy

from maze import Maze

from maze.color.colored_cell import CellColor
from maze.color.util import random_colored_cells
from model import Model
from model.factory import llm_model

from prompt import PromptGenerator
from prompt.config import PromptConfig

from maze.factory import create_dataset
from prompt.style.color import ColorStyle
from solver import PreambleLocation


@dataclass(frozen=True)
class ExperimentConfig:
    """
    Configuration for running experiments.

    Attributes:
        models (list[Model]): List of models to use in the experiment.
        prompt_generator (PromptGenerator): Prompt generator to use in the experiment.
        preamble_location (PreambleLocation): Where to place the problem preamble prompt.
        maze_sizes (list[int]): Maze sizes to use in the experiment (ignored if ExperimentConfig.mazes is not None).
        iterations (int): Number of trials to run per model per maze size.
        provide_history (bool): Whether to provide the model with the chat history or reset the model at every step.
        quiet (bool): Suppress verbose cli output during experiment execution.
        n_colors (Callable[[int], int] | None): Optional function mapping maze size to number of
            colored tiles per maze generated (ignored if ExperimentConfig.mazes is not None).
            If None, no colored tiles are placed in the mazes. Default: None.
        mazes (list[Maze] | None): Optional pre-generated mazes. If set it ignores ExperimentConfig.maze_sizes and ExperimentConfig.n_colors.
            If None, mazes are randomly generated based on maze_sizes during experiment. Default: None.
    """

    models: list[Model]
    prompt_generator: PromptGenerator
    preamble_location: PreambleLocation
    maze_sizes: list[int]
    iterations: int
    provide_history: bool
    quiet: bool
    n_colors: Callable[[int], int] | None = None
    mazes: list[Maze] | None = None


def load_config() -> ExperimentConfig:
    models = [
        llm_model("deepseek-r1:70b"),
    ]
    prompt_config = PromptConfig(
        provide_legal_output_hint=True,
        provide_spacial_awerness_hint=False,
        provide_color_hint=True,
        provide_repetition_hint=True,
        provide_steps_summary=0,
        provide_possible_moves=False,
        provide_cot_reminder=True,
    )
    prompt_style = ColorStyle()
    preamble_location = PreambleLocation.SYSTEM
    maze_sizes = [3]
    iterations = 10
    provide_history = True
    quiet = True
    return ExperimentConfig(
        models=models,
        prompt_generator=PromptGenerator(prompt_style, prompt_config),
        preamble_location=preamble_location,
        maze_sizes=maze_sizes,
        iterations=iterations,
        provide_history=provide_history,
        quiet=quiet,
        # n_colors=_calculate_n_colors,
        mazes=_maze_to_list(_hard_3x3_mazes()[0], 10),
    )


def _calculate_n_colors(maze_size: int) -> int:
    return min(round(maze_size * maze_size / 2), len(CellColor))


def _hard_3x3_mazes():
    colored_cells_number = 5
    colored_cells = random_colored_cells(1, 3, colored_cells_number)[0]
    mazes = create_dataset(10, 3, colored_cells=[colored_cells] * 10).mazes
    indexes = [4]
    return [maze for i, maze in enumerate(mazes) if i in indexes]


def _maze_to_list(maze: Maze, n: int) -> list[Maze]:
    filled_list: list[Maze] = []
    for _ in range(n):
        filled_list.append(deepcopy(maze))
    return filled_list
