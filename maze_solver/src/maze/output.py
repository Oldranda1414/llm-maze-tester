from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from rich.console import Console
from rich.text import Text

from maze import Maze
from maze.core.direction import Direction
from maze.core.navigation import neighbor, direction, exit_direction
from maze.core.coordinate import Coordinate


def save_maze(maze: Maze, save_path: str):
    fig, _ = draw_maze(maze)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")


def draw_maze(
    maze: Maze, ax: Axes | None = None, show_path: bool = True
) -> tuple[Figure, Axes]:
    if ax is None:
        plt.close("all")
        fig, ax = plt.subplots(figsize=(5, 5))
    else:
        fig = ax.figure
        assert isinstance(fig, Figure)

    grid_size = maze.size
    WALL_WIDTH = 3
    cell_size = 1.0

    ax.set_facecolor("white")

    t_i, t_j = maze.target
    e_direction = exit_direction(maze.target, maze.size)

    # Borders
    for j in range(grid_size):
        if not (e_direction == Direction.SOUTH and j == t_j):
            ax.plot([j, j + 1], [0, 0], "k-", linewidth=WALL_WIDTH)
        if not (e_direction == Direction.NORTH and j == t_j):
            ax.plot([j, j + 1], [grid_size, grid_size], "k-", linewidth=WALL_WIDTH)
    for i in range(grid_size):
        if not (e_direction == Direction.WEST and i == grid_size - t_i - 1):
            ax.plot([0, 0], [i, i + 1], "k-", linewidth=WALL_WIDTH)
        if not (e_direction == Direction.EAST and i == grid_size - t_i - 1):
            ax.plot([grid_size, grid_size], [i, i + 1], "k-", linewidth=WALL_WIDTH)

    # Cells
    cl = maze.connection_list
    for i in range(grid_size):
        for j in range(grid_size):
            y_plot = grid_size - i - 1
            facecolor = "yellow" if _is_seen((i, j), maze) else "white"
            rect = Rectangle(
                (j, y_plot),
                cell_size,
                cell_size,
                facecolor=facecolor,
                edgecolor="lightgray",
                linewidth=0.5,
            )
            ax.add_patch(rect)

            if j < grid_size - 1 and not cl.horizontal_passages[i][j]:
                ax.plot(
                    [j + 1, j + 1], [y_plot, y_plot + 1], "k-", linewidth=WALL_WIDTH
                )
            if i < grid_size - 1 and not cl.vertical_passages[i][j]:
                ax.plot([j, j + 1], [y_plot, y_plot], "k-", linewidth=WALL_WIDTH)

    # Start marker
    for pos, color, marker, label in [
        (maze.start, "darkorange", "o", "Start"),
    ]:
        if pos:
            pos_x, pos_y = pos
            x, y = _plot_coords(pos_x, pos_y, grid_size)
            ax.plot(
                x,
                y,
                marker,
                markersize=12,
                markeredgecolor=color,
                label=label,
                color=color,
            )

    if show_path:
        _draw_path(ax, maze)

    ax.set_xlim(-0.1, grid_size + 0.1)
    ax.set_ylim(-0.1, grid_size + 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Maze {grid_size}x{grid_size}")

    return fig, ax


def print_maze(maze: Maze) -> None:
    console = Console()
    grid_size = maze.size
    path = maze.path

    path_set = set(path)
    current_pos = path[-1] if path else None
    start_pos = maze.start
    target_pos = maze.target

    t_i, t_j = target_pos
    e_direction = exit_direction(maze.target, maze.size)

    for i in range(grid_size):
        top_line = Text()
        for j in range(grid_size):
            top_line.append("+")
            if i == 0 and e_direction == Direction.NORTH and j == t_j:
                top_line.append("   ")
            elif i == 0 or not maze.connection_list.vertical_passages[i - 1][j]:
                top_line.append("---")
            else:
                top_line.append("   ")
        top_line.append("+")
        console.print(top_line)

        mid_line = Text()
        for j in range(grid_size):
            if j == 0 and e_direction == Direction.WEST and i == grid_size - t_i - 1:
                mid_line.append(" ")
            elif j == 0 or not maze.connection_list.horizontal_passages[i][j - 1]:
                mid_line.append("|")
            else:
                mid_line.append(" ")

            coord = (i, j)
            if coord == current_pos:
                mid_line.append(" C ", style="bold green")
            elif coord == start_pos:
                mid_line.append(" S ", style="red")
            elif coord in path_set:
                mid_line.append(" · ", style="yellow")
            else:
                mid_line.append("   ")

        if e_direction == Direction.EAST and i == grid_size - t_i - 1:
            mid_line.append(" ")
        else:
            mid_line.append("|")
        console.print(mid_line)

    bottom = Text()
    for j in range(grid_size):
        bottom.append("+")
        if e_direction == Direction.SOUTH and j == t_j:
            bottom.append("   ")
        else:
            bottom.append("---")
    bottom.append("+")
    console.print(bottom)


def _draw_path(ax, maze: Maze):
    path = maze.path
    maze_size = maze.size
    if not path:
        return

    PATH_COLOR = "orange"
    CURRENT_COLOR = "green"
    PATH_ALPHA = 0.8

    # Draw path segments and points
    for i in range(len(path)):
        x, y = _plot_coords(*path[i], maze_size)
        if i > 0:
            px, py = _plot_coords(*path[i - 1], maze_size)
            ax.plot(
                [px, x],
                [py, y],
                color=PATH_COLOR,
                linewidth=8,
                alpha=PATH_ALPHA,
                solid_capstyle="round",
            )

        if i == len(path) - 1 and not maze.solved:
            ax.plot(
                x,
                y,
                "o",
                color=CURRENT_COLOR,
                markersize=10,
                alpha=PATH_ALPHA,
                markeredgecolor="darkgreen",
                markeredgewidth=2,
            )
        else:
            ax.plot(
                x,
                y,
                "o",
                color=PATH_COLOR,
                markersize=6,
                alpha=PATH_ALPHA,
                markeredgecolor="goldenrod",
                markeredgewidth=1,
            )


def _plot_coords(i: int, j: int, grid_size: int) -> tuple[float, float]:
    """Convert maze indices (i,j) to plotting coordinates (x,y)."""
    return j + 0.5, grid_size - i - 1 + 0.5


def _is_seen(cell: Coordinate, maze: Maze) -> bool:
    if maze.position == cell:
        return True

    cl = maze.connection_list
    position = maze.position
    d = direction(position, cell)
    distance = 0
    while d is not None and distance < maze.sight_depth:
        n = neighbor(position, d)
        if cl.connected(position, n):
            if n == cell:
                return True
            position = n
            distance += 1

        else:
            break

    return False
