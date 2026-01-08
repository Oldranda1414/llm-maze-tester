from maze.core.navigation import path_to_directions
from maze.factory import create_maze


def run() -> None:
    for seed in range(10):
        m = create_maze(seed=seed)
        solution = path_to_directions(m.solution)
        for cord in solution:
            m.move(cord)
        if m.position != m.target:
            print(f"Unsolved seed: {seed}")
            m.print()
