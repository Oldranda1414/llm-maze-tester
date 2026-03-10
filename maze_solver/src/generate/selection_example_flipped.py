from typing import cast
import matplotlib.pyplot as plt
from maze import Maze
from maze.factory import create_maze, _is_non_trivial
from maze.lattice_maze import LatticeMaze
from maze.output import draw_maze
from maze.core.navigation import exit_direction


def selection_example_flipped(path: str):
    maze_sizes = [3, 4, 5]
    maze_starts = [((1, 0), (0, 0)), ((2, 2), (3, 0)), ((0, 0), (1, 2))]

    mazes = generate_mazes(maze_sizes, maze_starts)
    titles = [
        "3x3 Scartato",
        "3x3 Valido",
        "4x4 Scartato",
        "4x4 Valido",
        "5x5 Scartato",
        "5x5 Valido",
    ]
    mazes = zip(mazes, titles)
    _, axes = plt.subplots(2, 3, figsize=(12, 8))

    for idx, (maze, title) in enumerate(mazes):
        row = idx % 2
        col = idx // 2
        draw_maze(
            maze,
            ax=axes[row][col],
            draw_character=True,
            highlight_seen_tiles=False,
            title=title,
        )

    plt.tight_layout()
    plt.savefig(f"{path}/selection_example_flipped.png", bbox_inches="tight", dpi=150)


def generate_mazes(
    maze_sizes: list[int], starts: list[tuple[tuple[int, int], tuple[int, int]]]
) -> list[Maze]:
    mazes: list[Maze] = []
    for maze_size, start_tuple in zip(maze_sizes, starts):
        filters = [is_trivial, _is_non_trivial]
        for filter, start in zip(filters, start_tuple):
            maze = cast(
                LatticeMaze,
                create_maze(size=maze_size, start=start, maze_filter=filter),
            )
            maze._set_path(maze.solution)
            last_move = exit_direction(maze.target, maze.size)
            maze.move(last_move)
            mazes.append(maze)
    return mazes


def is_trivial(maze: Maze) -> bool:
    return not _is_non_trivial(maze)
