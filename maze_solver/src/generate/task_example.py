import matplotlib.pyplot as plt

from maze.factory import create_maze
from maze.output import draw_maze


def task_example(path: str):
    maze_size = 6
    maze = create_maze(maze_size, start=(3, 1))
    prompt = "A nord c'è un corridoio che si estende per un metro.\n\nA est c'è un corridoio che si estende per due metri.\n\nA sud c'è un muro.\n\nA ovest c'è un muro."

    mazes = [(maze, prompt)]

    _, axes = plt.subplots(len(mazes), 2, figsize=(8, len(mazes) * 4))
    if len(mazes) == 1:
        axes = [axes]

    for i, (maze, text) in enumerate(mazes):
        draw_maze(maze, ax=axes[i][0], highlight_seen_tiles=False, title="")

        axes[i][1].text(0.0, 0.5, text, fontsize=18, va="center", wrap=True)
        axes[i][1].axis("off")

    plt.tight_layout()
    plt.savefig(f"{path}/task_example.png", bbox_inches="tight", dpi=150)
