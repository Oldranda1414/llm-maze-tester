from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from rich.console import Console
from rich.text import Text

from maze import Maze
from maze.colored_cell import CellColor
from maze.core.direction import Direction
from maze.core.navigation import neighbor, direction, exit_direction
from maze.core.coordinate import Coordinate

WALL_WIDTH = 3


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
    _draw_cells(ax, maze)

    _draw_start(ax, maze)
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


def _draw_cells(ax, maze: Maze):
    cell_size = 1.0
    cl = maze.connection_list
    grid_size = maze.size
    for i in range(grid_size):
        for j in range(grid_size):
            y_plot = grid_size - i - 1
            facecolor = "yellow" if _is_seen((i, j), maze) else "white"
            edgecolor = "lightgrey"
            rect = Rectangle(
                (j, y_plot),
                cell_size,
                cell_size,
                facecolor=facecolor,
                edgecolor=edgecolor,
                linewidth=0.5,
            )
            ax.add_patch(rect)

            cell_color = _cell_color((i, j), maze)
            if cell_color is not None:
                inner_border_color = cell_color.to_hex()
                inner_border_width = 2
                inner_padding = cell_size * 0.1

                inner_rect = Rectangle(
                    (j + inner_padding / 2, y_plot + inner_padding / 2),
                    cell_size - inner_padding,
                    cell_size - inner_padding,
                    facecolor="none",
                    edgecolor=inner_border_color,
                    linewidth=inner_border_width,
                    zorder=2,
                )
                ax.add_patch(inner_rect)

            if j < grid_size - 1 and not cl.horizontal_passages[i][j]:
                ax.plot(
                    [j + 1, j + 1], [y_plot, y_plot + 1], "k-", linewidth=WALL_WIDTH
                )
            if i < grid_size - 1 and not cl.vertical_passages[i][j]:
                ax.plot([j, j + 1], [y_plot, y_plot], "k-", linewidth=WALL_WIDTH)


def _draw_start(ax, maze: Maze):
    start_pos = maze.start
    grid_size = maze.size
    start_color = "#FF8C00"
    start_marker = "o"
    start_label = "Start"

    pos_x, pos_y = start_pos
    x, y = _plot_coords(pos_x, pos_y, grid_size)
    ax.plot(
        x,
        y,
        start_marker,
        markersize=12,
        markeredgecolor=start_color,
        label=start_label,
        color=start_color,
    )


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


def _cell_color(coord: Coordinate, maze: Maze) -> CellColor | None:
    colored_cells_coords: list[Coordinate] = [
        cell.coordinate for cell in maze.colored_cells
    ]
    colored_cells_dict: dict[Coordinate, CellColor] = {
        cell.coordinate: cell.color for cell in maze.colored_cells
    }
    if coord in colored_cells_coords:
        return colored_cells_dict[coord]
    return None
