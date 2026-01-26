from maze.factory import create_maze
from model.factory import llm_model
from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.narrative import NarrativeStyle
from solver import MazeSolver, PreambleLocation


def run() -> None:
    model = "llama3"
    size = 5
    i = 9

    solver = MazeSolver(
        llm_model(model),
        PromptGenerator(NarrativeStyle(), PromptConfig(True, True, False, 0, True)),
        create_maze(size=size, seed=i),
        PreambleLocation.SYSTEM,
        True,
    )
    solver.maze.print()
    print(len(solver.maze.solution))
