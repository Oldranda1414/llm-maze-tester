from copy import deepcopy
import html
import matplotlib.pyplot as plt
from chat_history import Exchange
from ipywidgets import interact, IntSlider, HTML
from IPython.display import display, clear_output

from maze import Maze
from maze.output import draw_maze
from move import Direction
from run import Run

def format_text(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")

def visualize_run(run: "Run"):
    """
    Interactive visualization for a Run object using matplotlib + ipywidgets.
    Displays maze state, system prompt, and chat messages with a slider to move through steps.
    """

    maze = run.maze
    chat = run.chat_history.chat
    num_steps = len(chat)

    message_html = HTML()

    def draw_step(step_idx: int):
        """Render maze and update text for the given step index."""
        clear_output(wait=True)

        # Draw maze with partial path up to this step
        partial_maze = deepcopy(maze)
        partial_maze = set_path(partial_maze, step_idx, chat)

        draw_maze(partial_maze, show_path=True)
        plt.show()

        # Update displayed messages
        if step_idx < len(chat):
            msg = chat[step_idx]
            message_html.value = (
                f"<h4>Prompt</h4><p>{format_text(msg.prompt)}</p>"
                f"<h4>Response</h4><p>{format_text(msg.response)}</p>"
            )
        else:
            message_html.value = ("<h4>Run finished</h4>")

        # Re-display UI (important for notebook interactivity)
        display(message_html)

    interact(
        draw_step,
        step_idx=IntSlider(min=0, max=max(num_steps, 0), step=1, value=0),
    )

def set_path(maze: Maze, step_idx: int, chat: list[Exchange]) -> Maze:
    maze.reset()
    for i in range(step_idx):
        response = chat[i].response
        next_move = Direction.from_coordinate(response[-1].upper())
        maze.move(next_move)
    return maze

