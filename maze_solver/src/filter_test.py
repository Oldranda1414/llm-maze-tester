from maze.factory import create_maze
from model.factory import llm_model
from prompt import PromptGenerator
from prompt.style.narrative import NarrativeStyle
from solver import MazeSolver

def main() -> None:
    model = "llama3"
    size = 5
    i = 9

    solver = MazeSolver(llm_model(model), PromptGenerator(NarrativeStyle()), create_maze(size=size, seed=i), True)
    solver.maze.print()
    print(len(solver.maze.solution))

if __name__ == "__main__":
    main()

