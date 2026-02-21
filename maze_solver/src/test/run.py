from maze.color.util import random_colored_cells
from maze.factory import create_maze
from model.factory import phony_model
from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.color import ColorStyle
from solver import MazeSolver, PreambleLocation
from run import Run


def run() -> None:
    run_path = "test_run.yaml"
    solver = MazeSolver(
        phony_model(),
        PromptGenerator(
            ColorStyle(), PromptConfig(True, True, True, True, True, 0, True, True)
        ),
        create_maze(colored_cells=random_colored_cells(1, 6, 10)[0]),
        PreambleLocation.SYSTEM,
    )
    while not solver.maze.solved:
        solver.step()
    solver.save_run(run_path, 60)
    run = Run.load(run_path)
    run.maze.print()
