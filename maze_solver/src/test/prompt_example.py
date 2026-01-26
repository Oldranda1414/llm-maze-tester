"""
Generates some example mazes with example prompts
"""

import matplotlib.pyplot as plt

from maze import Maze
from maze.factory import create_maze
from maze.output import draw_maze

from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.narrative import NarrativeStyle


def run() -> None:
    mazes: list[tuple[Maze, str]] = []
    prompt_generator = PromptGenerator(
        NarrativeStyle(), PromptConfig(True, True, False, 0, True)
    )
    for i in range(2, 7):
        sight_depth = 2
        m = create_maze(size=i, sight_depth=sight_depth)
        prompt = prompt_generator.step_prompt(m)
        mazes.append((m, prompt))

    _, axes = plt.subplots(len(mazes), 2, figsize=(8, len(mazes) * 4))
    if len(mazes) == 1:
        axes = [axes]

    for i, (maze, text) in enumerate(mazes):
        draw_maze(maze, ax=axes[i][0])

        axes[i][1].text(0.0, 0.5, text, fontsize=12, va="center", wrap=True)
        axes[i][1].axis("off")

    plt.tight_layout()
    plt.savefig("maze_summary.png", bbox_inches="tight", dpi=150)
