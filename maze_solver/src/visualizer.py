import html
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider, VBox, HTML
from IPython.display import display, clear_output

from maze.output import draw_maze
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
    path = maze.path()
    num_steps = len(path)

    # System prompt text (displayed once)
    prompt_html = HTML(f"<h4>System prompt</h4><p>{format_text(run.chat_history.system_prompt)}</p>")

    # Chat message output (changes per step)
    message_html = HTML()

    def draw_step(step_idx: int):
        """Render maze and update text for the given step index."""
        clear_output(wait=True)

        # Draw maze with partial path up to this step
        partial_maze = maze
        partial_maze.set_path(path[: step_idx + 1])

        draw_maze(partial_maze, show_path=True)
        plt.show()

        # Update displayed messages
        msg = chat[step_idx]
        test_response = msg.response + '\nsome\nlines\n\nsome more'
        message_html.value = (
            f"<h4>Prompt</h4><p>{format_text(msg.prompt)}</p>"
            f"<h4>Response</h4><p>{format_text(test_response)}</p>"
        )

        # Re-display UI (important for notebook interactivity)
        display(VBox([prompt_html, message_html]))

    interact(
        draw_step,
        step_idx=IntSlider(min=0, max=max(num_steps - 1, 0), step=1, value=0),
    )
