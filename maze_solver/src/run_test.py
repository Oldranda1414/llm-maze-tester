
from solver import MazeSolver
from run import Run


def main() -> None:
    run_path = 'test_run.yaml'
    solver = MazeSolver("llama3", debug=True)
    while not solver.maze.solved():
        solver.step()
    solver.save_run(run_path, 60)
    run = Run.load(run_path)
    print(run.chat_history)
    run.maze.print()

if __name__ == "__main__":
    main()

