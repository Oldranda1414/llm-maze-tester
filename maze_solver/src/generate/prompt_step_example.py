import matplotlib.pyplot as plt

from maze import Maze
from maze.core.direction import Direction
from maze.factory import create_maze
from maze.output import draw_maze

from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.narrative import NarrativeStyle


def prompt_step_example(path: str) -> None:
    mazes: list[tuple[Maze, str]] = []
    prompt_generator = PromptGenerator(
        NarrativeStyle(),
        PromptConfig(False, False, False, False, False, 0, False, False),
    )
    sight_depth = 1
    maze_size = 3
    start = (2, 2)
    steps = [Direction.NORTH, Direction.WEST]
    for i in range(len(steps)):
        m = create_maze(size=maze_size, start=start, sight_depth=sight_depth)
        prompt = ""
        for step_count in range(i + 1):
            m.move(steps[step_count])
        prompt += prompt_generator.last_move_info(m)
        prompt += prompt_generator.step_prompt(m)
        mazes.append((m, prompt))

    _, axes = plt.subplots(len(mazes), 2, figsize=(8, len(mazes) * 4))
    if len(mazes) == 1:
        axes = [axes]

    for i, (maze, text) in enumerate(mazes):
        draw_maze(maze, ax=axes[i][0])

        axes[i][1].text(0.0, 0.5, text, fontsize=12, va="center", wrap=True)
        axes[i][1].axis("off")

    plt.tight_layout()
    plt.savefig(f"{path}/prompt_step_example.png", bbox_inches="tight", dpi=150)
