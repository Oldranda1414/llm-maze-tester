from maze.factory import create_maze
from model.factory import phony_model
from prompt import PromptGenerator
from prompt.style.narrative import NarrativeStyle
from solver import MazeSolver
from run import Run

def run() -> None:
    run_path = 'test_run.yaml'
    solver = MazeSolver(phony_model("llama3"), PromptGenerator(NarrativeStyle()), create_maze())
    while not solver.maze.solved:
        solver.step()
    solver.save_run(run_path, 60)
    run = Run.load(run_path)
    run.maze.print()

