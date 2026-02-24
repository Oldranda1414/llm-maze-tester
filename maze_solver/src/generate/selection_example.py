from typing import cast
import matplotlib.pyplot as plt
from maze import Maze
from maze.factory import create_maze, _is_non_trivial
from maze.lattice_maze import LatticeMaze
from maze.output import draw_maze
from maze.core.navigation import exit_direction


def selection_example(path: str):
    maze_sizes = [3, 4, 5]

    mazes = generate_mazes(maze_sizes)
    _, axes = plt.subplots(3, 2, figsize=(8, 12))

    for idx, maze in enumerate(mazes):
        row = idx // 2
        col = idx % 2
        draw_maze(
            maze, ax=axes[row][col], draw_character=True, highlight_seen_tiles=False
        )

    plt.tight_layout()
    plt.savefig(f"{path}/selection_example.png", bbox_inches="tight", dpi=150)


def generate_mazes(maze_sizes: list[int]) -> list[Maze]:
    mazes: list[Maze] = []
    for maze_size in maze_sizes:
        filters = [is_trivial, _is_non_trivial]
        for filter in filters:
            maze = cast(LatticeMaze, create_maze(size=maze_size, maze_filter=filter))
            maze._set_path(maze.solution)
            last_move = exit_direction(maze.target, maze.size)
            maze.move(last_move)
            mazes.append(maze)
    return mazes


def is_trivial(maze: Maze) -> bool:
    return not _is_non_trivial(maze)
