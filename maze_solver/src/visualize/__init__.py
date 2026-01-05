
from copy import deepcopy
import html
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider, HTML, Output
from IPython.display import display, clear_output

from run import Run
from util import seconds_to_padded_time, set_path
from maze.output import draw_maze

def format_text(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")

def visualize_run(run: Run):

    maze = run.maze
    chat = run.chat_history.chat
    num_steps = len(chat)

    # ------------ STATIC BLOCK (does not update) ------------
    stats_html = HTML()

    stats_text = f"""
    <div style="padding: 10px; border-radius: 5px; margin-bottom: 10px;">
        <h3>Run Statistics</h3>
        <table style="width: 100%;">
            <tr>
                <td><strong>Maze Dimension:</strong></td>
                <td>{run.maze_size}x{run.maze_size}</td>
                <td><strong>Start Position:</strong></td>
                <td>{run.start_position}</td>
            </tr>
            <tr>
                <td><strong>Target Position:</strong></td>
                <td>{run.target_position}</td>
                <td><strong>Current Position:</strong></td>
                <td>{run.current_position}</td>
            </tr>
            <tr>
                <td><strong>Solved:</strong></td>
                <td>{'Yes' if run.is_solved else 'No'}</td>
                <td><strong>Unique Positions Visited:</strong></td>
                <td>{run.unique_positions_visited}</td>
            </tr>
            <tr>
                <td><strong>Illegal Directions:</strong></td>
                <td>{run.illegal_directions}</td>
                <td><strong>Illegal Responses:</strong></td>
                <td>{run.illegal_responses}</td>
            </tr>
            <tr>
                <td><strong>Total Steps:</strong></td>
                <td>{num_steps}</td>
                <td><strong>Path Length:</strong></td>
                <td>{len(maze.path)}</td>
            </tr>
            <tr>
                <td><strong>Execution Time</strong></td>
                <td>{seconds_to_padded_time(run.execution_time)}</td>
            </tr>
        </table>
    </div>
    """

    stats_html.value = stats_text

    # ------------ DYNAMIC OUTPUT AREAS ------------
    maze_out = Output()
    msg_out = Output()

    # ------------ UPDATE FUNCTION ------------
    def draw_step(step_idx):

        # Update maze
        with maze_out:
            clear_output(wait=True)
            partial_maze = deepcopy(maze)
            partial_maze = set_path(partial_maze, chat, step_idx)
            draw_maze(partial_maze, show_path=True)
            plt.show()

        # Update messages
        with msg_out:
            clear_output(wait=True)
            if step_idx < len(chat):
                msg = chat[step_idx]
                html_block = (
                    f"<h4>Prompt</h4><p>{format_text(msg.prompt)}</p>"
                    f"<h4>Response</h4><p>{format_text(msg.response)}</p>"
                )
            else:
                html_block = "<h4>Run finished</h4>"

            display(HTML(html_block))

    # ------------ SLIDER ------------
    interact(
        draw_step,
        step_idx=IntSlider(min=0, max=max(num_steps, 0), step=1, value=0),
    )

    display(stats_html, maze_out, msg_out)

