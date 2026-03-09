import matplotlib.pyplot as plt

from maze import Maze
from maze.factory import create_maze
from maze.output import draw_maze

from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.narrative import NarrativeStyle


def prompt_example_flipped(path: str) -> None:
    mazes: list[tuple[Maze, str]] = []
    prompt_generator = PromptGenerator(
        NarrativeStyle(),
        PromptConfig(False, False, False, False, False, 0, False, False),
    )
    sight_depth = 1
    maze_size = 3
    start = (2, 2)

    m = create_maze(size=maze_size, start=start, sight_depth=sight_depth)
    prompt = ""
    prompt += prompt_generator.get_preamble(m)
    prompt += prompt_generator.step_prompt(m)
    mazes.append((m, prompt))

    _, axes = plt.subplots(2, len(mazes), figsize=(len(mazes) * 5, 8))

    if len(mazes) == 1:
        axes = [[axes[0]], [axes[1]]]

    for i, (maze, text) in enumerate(mazes):
        draw_maze(maze, ax=axes[0][i])

        axes[1][i].text(0.0, 1.0, text, fontsize=12, va="top", wrap=True)
        axes[1][i].axis("off")

    plt.tight_layout()
    plt.savefig(f"{path}/prompt_example_flipped.png", bbox_inches="tight", dpi=150)
