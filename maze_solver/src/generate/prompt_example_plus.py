import matplotlib.pyplot as plt

from maze import Maze
from maze.factory import create_maze
from maze.output import draw_maze

from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.narrative import NarrativeStyle


def prompt_example_plus(path: str) -> None:
    mazes: list[tuple[Maze, str, str]] = []
    prompt_generator = PromptGenerator(
        NarrativeStyle(),
        PromptConfig(False, False, False, False, False, 0, False, False),
    )

    sight_depth = 1
    maze_size = 3
    start = (2, 2)
    title = "passo 0"

    m = create_maze(size=maze_size, start=start, sight_depth=sight_depth)
    prompt = ""
    prompt += prompt_generator.get_preamble(m)
    prompt += prompt_generator.step_prompt(m)
    mazes.append((m, prompt, title))

    n = len(mazes)

    fig = plt.figure(figsize=(10, n * 8))
    gs = fig.add_gridspec(
        nrows=n * 2,
        ncols=1,
        height_ratios=[5, 3] * n,  # fixed maze/text ratio for each example
    )

    axes = [fig.add_subplot(gs[i, 0]) for i in range(n * 2)]

    for i, (maze, text, title) in enumerate(mazes):
        maze_ax = axes[i * 2]
        text_ax = axes[i * 2 + 1]

        draw_maze(maze, ax=maze_ax, title=title)

        text_ax.text(
            0.0,
            1.0,
            text,
            fontsize=12,
            va="top",
            ha="left",
            wrap=True,
            transform=text_ax.transAxes,
        )
        text_ax.axis("off")

    fig.tight_layout()
    fig.savefig(f"{path}/prompt_example_plus.png", bbox_inches="tight", dpi=150)
