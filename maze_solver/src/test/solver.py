from model.factory import phony_model
from maze.factory import create_maze
from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.narrative import NarrativeStyle
from solver import MazeSolver, PreambleLocation


def run():
    maze_size = 3
    sight_depth = 3
    model = phony_model()
    maze = create_maze(size=maze_size, sight_depth=sight_depth)
    pg = PromptGenerator(NarrativeStyle(), PromptConfig(True, True, False, 0, True))
    maze_solver = MazeSolver(model, pg, maze, PreambleLocation.SYSTEM)
    while not maze_solver.is_solved():
        maze_solver.step()
