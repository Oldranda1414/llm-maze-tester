import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from maze_dataset.maze import TargetedLatticeMaze
from move import Coordinate

def save_maze_cell_based(maze: TargetedLatticeMaze, path: list[Coordinate], save_path: str):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(5, 5))
    
    grid_size = maze.grid_shape[0]  # Assuming square maze
    cell_size = 1.0
    
    ax.set_facecolor('white')
    
    # Draw outer border
    ax.plot([0, grid_size], [0, 0], 'k-', linewidth=3)  # bottom
    ax.plot([0, grid_size], [grid_size, grid_size], 'k-', linewidth=3)  # top
    ax.plot([0, 0], [0, grid_size], 'k-', linewidth=3)  # left
    ax.plot([grid_size, grid_size], [0, grid_size], 'k-', linewidth=3)  # right
    
    # Draw internal walls
    for i in range(grid_size):
        for j in range(grid_size):
            y_plot = grid_size - i - 1  # flip vertically for plotting
            
            # Cell background
            rect = plt.Rectangle((j, y_plot), cell_size, cell_size, 
                                 facecolor='white', edgecolor='lightgray', linewidth=0.5)
            ax.add_patch(rect)
            
            # RIGHT wall – only if no connection
            if j < grid_size - 1:
                if not maze.connection_list[1, i, j]:  # use 1 for horizontal (right)
                    ax.plot([j + 1, j + 1], [y_plot, y_plot + 1], 'k-', linewidth=3)
            
            # BOTTOM wall – only if no connection
            if i < grid_size - 1:
                if not maze.connection_list[0, i, j]:  # use 0 for vertical (down)
                    ax.plot([j, j + 1], [y_plot, y_plot], 'k-', linewidth=3)
    
    # Draw path
    _draw_path_cell_based(ax, path, grid_size, cell_size)
    
    # Draw start and target markers
    if hasattr(maze, 'start') and maze.start is not None:
        sy = grid_size - maze.start[0] - 1 + 0.5
        sx = maze.start[1] + 0.5
        ax.plot(sx, sy, 'go', markersize=12, markeredgecolor='darkgreen', label='Start')
    
    if hasattr(maze, 'target') and maze.target is not None:
        ty = grid_size - maze.target[0] - 1 + 0.5
        tx = maze.target[1] + 0.5
        ax.plot(tx, ty, 'rs', markersize=12, markeredgecolor='darkred', label='Target')
    
    ax.set_xlim(-0.1, grid_size + 0.1)
    ax.set_ylim(-0.1, grid_size + 0.1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"Maze {grid_size}x{grid_size}")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')

def print_maze_cell_based(maze: TargetedLatticeMaze, path: list[Coordinate]):
    """ASCII/terminal maze printer consistent with the cell-based plotting logic.

    Assumptions:
      - maze.connection_list[0, i, j] is a boolean: connection DOWN from (i,j) to (i+1, j)
      - maze.connection_list[1, i, j] is a boolean: connection RIGHT from (i,j) to (i, j+1)
      - logical coordinates: (i, j) with i=0 being the top row, i increasing downward
    """
    from rich.console import Console
    from rich.text import Text

    console = Console()
    grid_size = maze.grid_shape[0]

    path_set = set(path)
    current_pos = path[-1] if path else None
    start_pos = getattr(maze, "start", None)
    target_pos = getattr(maze, "target", None)

    # Print rows from top (i=0) to bottom (i=grid_size-1)
    for i in range(grid_size):
        # Top border for this row
        top_line = Text()
        for j in range(grid_size):
            top_line.append("+")
            if i == 0:
                # top-most logical row -> top border
                top_line.append("---")
            else:
                # If the cell above (i-1, j) connects DOWN to this cell, no top wall
                if maze.connection_list[0, i - 1, j]:
                    top_line.append("   ")
                else:
                    top_line.append("---")
        top_line.append("+")
        console.print(top_line)

        # Mid line: left wall, cell content, repeated
        mid_line = Text()
        for j in range(grid_size):
            # Left border for first column
            if j == 0:
                mid_line.append("|")
            else:
                # If the cell to the left (i, j-1) connects RIGHT to current, no left wall
                if maze.connection_list[1, i, j - 1]:
                    mid_line.append(" ")
                else:
                    mid_line.append("|")

            # Cell content: Current (C), Start (S), Target (T), path dot, or empty
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

        # Right-most border
        mid_line.append("|")
        console.print(mid_line)

    # Bottom border after all rows
    bottom_line = Text()
    for j in range(grid_size):
        bottom_line.append("+")
        bottom_line.append("---")
    bottom_line.append("+")
    console.print(bottom_line)

def _draw_path_cell_based(ax, path: list[Coordinate], grid_size: int, cell_size: float):
    """Draw the path on the maze"""
    if not path:
        return
    
    PATH_COLOR = 'gold'
    CURRENT_COLOR = 'darkorange'
    PATH_ALPHA = 0.8
    
    # Draw path segments (lines between cells)
    for i in range(len(path) - 1):
        current = path[i]
        next_cell = path[i + 1]
        
        # Convert to plot coordinates (flip y-axis)
        current_plot = (current[1] + 0.5, grid_size - current[0] - 1 + 0.5)
        next_plot = (next_cell[1] + 0.5, grid_size - next_cell[0] - 1 + 0.5)
        
        ax.plot([current_plot[0], next_plot[0]], [current_plot[1], next_plot[1]], 
               color=PATH_COLOR, linewidth=8, alpha=PATH_ALPHA, solid_capstyle='round')
    
    # Draw path points (circles on cells)
    for i, coord in enumerate(path):
        x = coord[1] + 0.5
        y = grid_size - coord[0] - 1 + 0.5
        
        if i == len(path) - 1:  # Current position
            ax.plot(x, y, 'o', color=CURRENT_COLOR, markersize=10, 
                   alpha=PATH_ALPHA, markeredgecolor='darkorange', markeredgewidth=2)
        else:  # Path history
            ax.plot(x, y, 'o', color=PATH_COLOR, markersize=6, 
                   alpha=PATH_ALPHA, markeredgecolor='goldenrod', markeredgewidth=1)


# Update main functions
def save_maze(maze: TargetedLatticeMaze, path: list[Coordinate], save_path: str):
    save_maze_cell_based(maze, path, save_path)

def print_maze(maze: TargetedLatticeMaze, path: list[Coordinate]):
    print_maze_cell_based(maze, path)

