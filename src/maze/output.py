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

    # Outer border
    ax.plot([0, grid_size], [0, 0], 'k-', linewidth=WALL_WIDTH)
    ax.plot([0, grid_size], [grid_size, grid_size], 'k-', linewidth=WALL_WIDTH)
    ax.plot([0, 0], [0, grid_size], 'k-', linewidth=WALL_WIDTH)
    ax.plot([grid_size, grid_size], [0, grid_size], 'k-', linewidth=WALL_WIDTH)

    # Internal walls
    for i in range(grid_size):
        for j in range(grid_size):
            y_plot = grid_size - i - 1
            rect = plt.Rectangle((j, y_plot), cell_size, cell_size,
                                 facecolor='white', edgecolor='lightgray', linewidth=0.5)
            ax.add_patch(rect)

            # Right wall
            if j < grid_size - 1 and not maze.connection_list()[1, i, j]:
                ax.plot([j + 1, j + 1], [y_plot, y_plot + 1], 'k-', linewidth=WALL_WIDTH)
            # Bottom wall
            if i < grid_size - 1 and not maze.connection_list()[0, i, j]:
                ax.plot([j, j + 1], [y_plot, y_plot], 'k-', linewidth=WALL_WIDTH)

    _draw_path(ax, maze.path(), grid_size)

    # Start / target markers
    for pos, color, marker, label in [
        (maze.start, "green", "o", "Start"),
        (maze.target, "red", "s", "Target")
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


# === ASCII Version ===

def print_maze(maze: Maze):
    """ASCII/terminal maze printer consistent with the plotting logic."""
    console = Console()
    grid_size = maze.size
    path = maze.path()

    path_set = set(path)
    current_pos = path[-1] if path else None
    start_pos = maze.start
    target_pos = maze.target

    for i in range(grid_size):
        # Top wall row
        top_line = Text()
        for j in range(grid_size):
            top_line.append("+")
            if i == 0 or not maze.connection_list()[0, i - 1, j]:
                top_line.append("---")
            else:
                top_line.append("   ")
        top_line.append("+")
        console.print(top_line)

        # Cell row
        mid_line = Text()
        for j in range(grid_size):
            if j == 0 or not maze.connection_list()[1, i, j - 1]:
                mid_line.append("|")
            else:
                mid_line.append(" ")

            coord = (i, j)
            if coord == current_pos:
                mid_line.append(" C ", style="bold red")
            elif coord == start_pos:
                mid_line.append(" S ", style="green")
            elif coord == target_pos:
                mid_line.append(" T ", style="bold magenta")
            elif coord in path_set:
                mid_line.append(" · ", style="yellow")
            else:
                mid_line.append("   ")

        mid_line.append("|")
        console.print(mid_line)

    # Bottom border
    bottom = Text("".join(["+---" * grid_size + "+"]))
    console.print(bottom)

def _plot_coords(i: int, j: int, grid_size: int) -> tuple[float, float]:
    """Convert maze indices (i,j) to plotting coordinates (x,y)."""
    return j + 0.5, grid_size - i - 1 + 0.5

