from maze.factory import create_maze
from prompt import PromptGenerator
from prompt.config import PromptConfig
from solver import MazeSolver, PreambleLocation
from model.factory import phony_model
from prompt.style.narrative import NarrativeStyle
from prompt.facts import _extract_lateral_paths


def run():
    solver = MazeSolver(
        phony_model(),
        PromptGenerator(
            NarrativeStyle(), PromptConfig(False, False, False, False, 0, False)
        ),
        create_maze(),
        PreambleLocation.SYSTEM,
        True,
    )
    while not solver.is_solved():
        solver.step()
        maze = solver.maze
        maze.print()
        for direction in maze.available_directions():
            print(direction, ":", _extract_lateral_paths(direction, maze))
