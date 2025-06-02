"""entry point for the program
"""

from maze_solver import MazeSolver


def main():
    """placeholder for real stuff
    """
    # Create a model instance with a lightweight model for testing
    # Using llama2 as it's commonly available, but you can change to any model you prefer
    model_name = "llama3:latest"
    print(f"Initializing model: {model_name}")

    maze_solver = MazeSolver(model_name=model_name, block_on_plot=True)
    print("Maze solver initialized. Starting to solve the maze...")

    while maze_solver.solved() is False:
        maze_solver.step()
        maze_solver.get_statistics()

    print("Maze solved!")

if __name__ == "__main__":
    main()
