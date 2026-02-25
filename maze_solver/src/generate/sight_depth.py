from copy import deepcopy
from typing import cast
import matplotlib.pyplot as plt
from maze import Maze
from maze.factory import create_maze, _is_non_trivial
from maze.lattice_maze import LatticeMaze
from maze.output import draw_maze


def sight_depth(path: str):
    maze_sizes = [3, 4, 5]
    maze_starts = [(2, 2), (0, 2), (4, 4)]

    mazes = generate_mazes(maze_sizes, maze_starts)
    _, axes = plt.subplots(3, 2, figsize=(8, 12))

    for idx, maze in enumerate(mazes):
        row = idx // 2
        col = idx % 2
        draw_maze(
            maze, ax=axes[row][col], draw_character=True, highlight_seen_tiles=True
        )

    plt.tight_layout()
    plt.savefig(f"{path}/sight_depth.png", bbox_inches="tight", dpi=150)


def generate_mazes(
    maze_sizes: list[int], maze_starts: list[tuple[int, int]]
) -> list[Maze]:
    mazes: list[Maze] = []
    for i in range(len(maze_sizes)):
        sight_depths = [1, 5]
        maze = create_maze(size=maze_sizes[i], start=maze_starts[i])
        maze = create_maze(size=maze_sizes[i], start=maze_starts[i])
        for sight_depth in sight_depths:
            modified = cast(LatticeMaze, deepcopy(maze))
            modified._sight_depth = sight_depth
            mazes.append(modified)
    return mazes


def is_trivial(maze: Maze) -> bool:
    return not _is_non_trivial(maze)
