import random
from maze.color.colored_cell import CellColor, ColoredCell
from maze.core.coordinate import Coordinate


def random_colored_cells(
    n_mazes: int, maze_size: int, n_colored_cells: int, seed: int = 42
) -> list[list[ColoredCell]]:
    rng = random.Random(seed)
    if n_colored_cells > len(CellColor):
        raise ValueError(
            f"n_colored_cells cannot be bigger then the available number of colors ({len(CellColor)})"
        )
    colored_cells: list[list[ColoredCell]] = []
    for _ in range(n_mazes):
        coords = _unique_random_coordinates(maze_size, n_colored_cells, rng)
        colors = rng.sample(list(CellColor), n_colored_cells)
        colored_cells.append(
            [ColoredCell(coord, color) for coord, color in zip(coords, colors)]
        )

    return colored_cells


def get_cell_color(
    coord: Coordinate, colored_cells: list[ColoredCell]
) -> CellColor | None:
    colored_cells_coords: list[Coordinate] = [cell.coordinate for cell in colored_cells]
    colored_cells_dict: dict[Coordinate, CellColor] = {
        cell.coordinate: cell.color for cell in colored_cells
    }
    if coord in colored_cells_coords:
        return colored_cells_dict[coord]
    return None


def _unique_random_coordinates(
    max_val: int, n: int, rng: random.Random
) -> list[Coordinate]:
    max_possible_tuples = max_val * max_val
    if n > max_possible_tuples:
        raise ValueError(
            f"Cannot generate {n} unique tuples. "
            f"Maximum possible with max_val={max_val} is {max_possible_tuples}"
        )

    # Use a set to ensure uniqueness
    unique_coordinates = set()

    # Generate tuples until we have n unique ones
    while len(unique_coordinates) < n:
        coordinate_val = (rng.randrange(max_val), rng.randrange(max_val))
        unique_coordinates.add(coordinate_val)

    return list(unique_coordinates)
