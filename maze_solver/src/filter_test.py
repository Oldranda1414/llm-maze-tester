from prompt.style.narrative import NarrativeStyle
from solver import MazeSolver

def main() -> None:
    model = "llama3"
    size = 5
    i = 9

    solver = MazeSolver(model_name=model, prompt_style=NarrativeStyle(), maze_size=size, seed=i, quiet=True)
    solver.maze.print()
    print(len(solver.maze.solution))

if __name__ == "__main__":
    main()

