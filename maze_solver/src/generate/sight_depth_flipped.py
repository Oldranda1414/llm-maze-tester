from copy import deepcopy
from typing import cast
import matplotlib.pyplot as plt
from maze import Maze
from maze.factory import create_maze, _is_non_trivial
from maze.lattice_maze import LatticeMaze
from maze.output import draw_maze


def sight_depth_flipped(path: str):
    maze_sizes = [3, 4, 5]
    maze_starts = [(2, 2), (0, 2), (4, 4)]

    mazes = generate_mazes(maze_sizes, maze_starts)
    titles = [
        "3x3 con d=1",
        "3x3 con d=5",
        "4x4 con d=1",
        "4x4 con d=5",
        "5x5 con d=1",
        "5x5 con d=5",
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
            highlight_seen_tiles=True,
            title=title,
        )

    plt.tight_layout()
    plt.savefig(f"{path}/sight_depth_flipped.png", bbox_inches="tight", dpi=150)


def generate_mazes(
    maze_sizes: list[int], maze_starts: list[tuple[int, int]]
) -> list[Maze]:
    mazes: list[Maze] = []
    for i in range(len(maze_sizes)):
        sight_depths = [1, 5]
        maze = create_maze(size=maze_sizes[i], start=maze_starts[i])
        for sight_depth in sight_depths:
            modified = cast(LatticeMaze, deepcopy(maze))
            modified._sight_depth = sight_depth
            mazes.append(modified)
    return mazes


def is_trivial(maze: Maze) -> bool:
    return not _is_non_trivial(maze)
