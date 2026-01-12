from copy import deepcopy
import textwrap
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt

from chat_history import Exchange
from maze import Maze
from maze.output import draw_maze
from run import Run
from util import execute_history


def draw_frame(
    step_idx: int,
    maze: Maze,
    chat: list[Exchange],
    system_prompt: str,
    ax_maze: Axes,
    ax_text: Axes,
):
    ax_maze.clear()
    ax_text.clear()

    # ----- Maze -----
    partial_maze = deepcopy(maze)
    partial_maze = execute_history(partial_maze, chat, step_idx)
    draw_maze(partial_maze, ax=ax_maze, show_path=True)

    # ----- Text -----
    if step_idx < len(chat):
        msg = chat[step_idx]

        if step_idx == 0:
            text = (
                "SYSTEM PROMPT\n"
                f"{system_prompt}\n\n"
                "PROMPT\n"
                f"{msg.prompt}\n\n"
                "RESPONSE\n"
                f"{msg.response}"
            )
        else:
            text = f"PROMPT\n{msg.prompt}\n\nRESPONSE\n{msg.response}"
    else:
        text = "RUN FINISHED"

    # Preserve paragraphing and wrap each line
    lines = text.split("\n")
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(textwrap.wrap(line, width=80))
    text = "\n".join(wrapped_lines)

    ax_text.text(
        0.01,
        0.99,
        text,
        va="top",
        ha="left",
        fontsize=8,
        fontfamily=["DejaVu Sans Mono", "Noto Sans CJK JP"],
        wrap=True,
    )

    ax_text.axis("off")


def run_to_mp4(
    run: Run,
    filename: str = "maze_run.mp4",
    fps: int = 1,
    fig_width: int = 10,
    fig_height: int = 7,
    text_ratio: float = 1.5,
) -> None:
    fig = plt.figure(figsize=(fig_width, fig_height))
    gs = GridSpec(1, 2, width_ratios=[1, text_ratio])

    ax_maze = fig.add_subplot(gs[0, 0])
    ax_text = fig.add_subplot(gs[0, 1])

    def update(step_idx: int) -> list[Artist]:
        draw_frame(
            step_idx,
            run.maze,
            run.chat_history.chat,
            run.chat_history.system_prompt,
            ax_maze,
            ax_text,
        )
        return []

    anim = FuncAnimation(
        fig,
        update,
        frames=len(run.chat_history.chat) + 1,
        interval=1000,
        blit=False,
    )

    writer = FFMpegWriter(
        fps=fps,
        metadata={"artist": "Maze Runner"},
        bitrate=1800,
    )

    anim.save(filename, writer=writer)
    plt.close(fig)
