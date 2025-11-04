import matplotlib.pyplot as plt

from maze import Maze

from rich.console import Console
from rich.text import Text

from move import Coordinate

def save_maze(maze: Maze, save_path: str):
    plt.close('all')
    _, ax = plt.subplots(figsize=(5, 5))

    grid_size = maze.size
    WALL_WIDTH = 3
    cell_size = 1.0

    ax.set_facecolor('white')

    t_i, t_j = maze.target
    exit_top = (t_i == 0)
    exit_bottom = (t_i == grid_size - 1)
    exit_left = (t_j == 0)
    exit_right = (t_j == grid_size - 1)
    if exit_top or exit_bottom:
        exit_left = False
        exit_right = False

    for j in range(grid_size):
        if not (exit_bottom and j == t_j):
            ax.plot([j, j + 1], [0, 0], 'k-', linewidth=WALL_WIDTH)
        if not (exit_top and j == t_j):
            ax.plot([j, j + 1], [grid_size, grid_size], 'k-', linewidth=WALL_WIDTH)
    for i in range(grid_size):
        if not (exit_left and i == grid_size - t_i - 1):
            ax.plot([0, 0], [i, i + 1], 'k-', linewidth=WALL_WIDTH)
        if not (exit_right and i == grid_size - t_i - 1):
            ax.plot([grid_size, grid_size], [i, i + 1], 'k-', linewidth=WALL_WIDTH)

    for i in range(grid_size):
        for j in range(grid_size):
            y_plot = grid_size - i - 1
            rect = plt.Rectangle((j, y_plot), cell_size, cell_size,
                                 facecolor='white', edgecolor='lightgray', linewidth=0.5)
            ax.add_patch(rect)

            if j < grid_size - 1 and not maze.connection_list().horizontal[i][j]:
                ax.plot([j + 1, j + 1], [y_plot, y_plot + 1], 'k-', linewidth=WALL_WIDTH)
            if i < grid_size - 1 and not maze.connection_list().vertical[i][j]:
                ax.plot([j, j + 1], [y_plot, y_plot], 'k-', linewidth=WALL_WIDTH)

    _draw_path(ax, maze.path(), grid_size)

    for pos, color, marker, label in [
        (maze.start, "green", "o", "Start"),
    ]:
        if pos:
            x, y = _plot_coords(*pos, grid_size)
            ax.plot(x, y, marker, markersize=12, markeredgecolor=color, label=label, color=color)

    ax.set_xlim(-0.1, grid_size + 0.1)
    ax.set_ylim(-0.1, grid_size + 0.1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"Maze {grid_size}x{grid_size}")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')

def print_maze(maze: Maze):
    console = Console()
    grid_size = maze.size
    path = maze.path()

    path_set = set(path)
    current_pos = path[-1] if path else None
    start_pos = maze.start
    target_pos = maze.target

    t_i, t_j = target_pos
    exit_top = (t_i == 0)
    exit_bottom = (t_i == grid_size - 1)
    exit_left = (t_j == 0)
    exit_right = (t_j == grid_size - 1)
    if exit_top or exit_bottom:
        exit_left = False
        exit_right = False

    for i in range(grid_size):
        top_line = Text()
        for j in range(grid_size):
            top_line.append("+")
            if (i == 0 and exit_top and j == t_j):
                top_line.append("   ")
            elif i == 0 or not maze.connection_list().vertical[i - 1][j]:
                top_line.append("---")
            else:
                top_line.append("   ")
        top_line.append("+")
        console.print(top_line)

        mid_line = Text()
        for j in range(grid_size):
            if (j == 0 and exit_left and i == grid_size - t_i - 1):
                mid_line.append(" ")
            elif j == 0 or not maze.connection_list().horizontal[i][j - 1]:
                mid_line.append("|")
            else:
                mid_line.append(" ")

            coord = (i, j)
            if coord == current_pos:
                mid_line.append(" C ", style="bold red")
            elif coord == start_pos:
                mid_line.append(" S ", style="green")
            elif coord in path_set:
                mid_line.append(" · ", style="yellow")
            else:
                mid_line.append("   ")

        if exit_right and i == grid_size - t_i - 1:
            mid_line.append(" ")
        else:
            mid_line.append("|")
        console.print(mid_line)

    bottom = Text()
    for j in range(grid_size):
        bottom.append("+")
        if exit_bottom and j == t_j:
            bottom.append("   ")
        else:
            bottom.append("---")
    bottom.append("+")
    console.print(bottom)

def _draw_path(ax, path: list[Coordinate], grid_size: int):
    if not path:
        return

    PATH_COLOR = 'gold'
    CURRENT_COLOR = 'darkorange'
    PATH_ALPHA = 0.8

    # Draw path segments and points
    for i in range(len(path)):
        x, y = _plot_coords(*path[i], grid_size)
        if i > 0:
            px, py = _plot_coords(*path[i - 1], grid_size)
            ax.plot([px, x], [py, y], color=PATH_COLOR, linewidth=8, alpha=PATH_ALPHA, solid_capstyle='round')

        if i == len(path) - 1:
            ax.plot(x, y, 'o', color=CURRENT_COLOR, markersize=10,
                    alpha=PATH_ALPHA, markeredgecolor='darkorange', markeredgewidth=2)
        else:
            ax.plot(x, y, 'o', color=PATH_COLOR, markersize=6,
                    alpha=PATH_ALPHA, markeredgecolor='goldenrod', markeredgewidth=1)


def _plot_coords(i: int, j: int, grid_size: int) -> tuple[float, float]:
    """Convert maze indices (i,j) to plotting coordinates (x,y)."""
    return j + 0.5, grid_size - i - 1 + 0.5

