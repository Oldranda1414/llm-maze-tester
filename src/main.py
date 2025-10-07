"""entry point for the program
"""

from maze_solver import MazeSolver


def main():
    """placeholder for real stuff
    """
    # Create a model instance with a lightweight model for testing
    # Using llama2 as it's commonly available, but you can change to any model you prefer
    model_name = "llama3:latest"
    maze_width = 3
    maze_height = 3
    print(f"Initializing model: {model_name}")

    maze_solver = MazeSolver(model_name=model_name, maze_width=maze_width, maze_height=maze_height)
    print("Maze solver initialized. Starting to solve the maze...")

    step = 0
    while maze_solver.solved() is False:
        maze_solver.step()
        step += 1
        if step % 20 == 0:
            print(maze_solver.get_statistics())
            maze_solver.maze.print()

    print("Maze solved!")

if __name__ == "__main__":
    main()
