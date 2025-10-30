import matplotlib.pyplot as plt
import numpy as np

from jaxtyping import Int
from maze_dataset.maze import TargetedLatticeMaze

from rich.console import Console
from rich.text import Text

from move import Coordinate

def save_maze(maze: TargetedLatticeMaze, path: list[Coordinate], save_path: str):
    pixels = _add_path(maze.as_pixels(), path)

    plt.close('all')
    plt.figure(figsize=(5, 5))

    plt.imshow(pixels, cmap='gray')
    plt.title(f"Maze {maze.grid_shape}x{maze.grid_shape}")
    plt.axis('off')

    plt.savefig(save_path, dpi=300, bbox_inches='tight')

def print_maze(maze: TargetedLatticeMaze, path: list[Coordinate]):
    pixels = _add_path(maze.as_pixels(), path)
    console = Console()
    for row in pixels:
        text_line = Text()
        for pixel in row:
            r, g, b = pixel[:3]
            text_line.append("  ", style=f"on rgb({r},{g},{b})")
        console.print(text_line)

def _add_path(pixel_maze: Int[np.ndarray, 'x y rgb'], path: list[Coordinate]) -> Int[np.ndarray, 'x y rgb']:
    PATH_COLOR = np.array([255, 255, 0], dtype=np.uint8)
    CURRENT_COLOR = np.array([255, 165, 0], dtype=np.uint8)
    result = pixel_maze.copy()
    scaling_factor = 2
    
    for index, coord in enumerate(path):
        row, col = coord
        center_row = row * scaling_factor + 1
        center_col = col * scaling_factor + 1
        
        if (0 <= center_row < result.shape[0] and 
            0 <= center_col < result.shape[1]):
            result[center_row, center_col] = PATH_COLOR if (index != len(path) - 1) else CURRENT_COLOR

    return result

