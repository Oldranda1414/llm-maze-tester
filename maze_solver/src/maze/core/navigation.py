from maze.core.coordinate import Coordinate
from maze.core.direction import Direction, get_offsets

def neighbor(cell: Coordinate, direction: Direction) -> Coordinate:
    dr, dc = get_offsets(direction)
    r, c = cell
    return (r + dr, c + dc)

def direction(start: Coordinate, target: Coordinate) -> Direction | None:
    """
    Returns the direction from start to target if one exists, None otherwise
    """
    (r1, c1), (r2, c2) = start, target
    dr, dc = r2 - r1, c2 - c1

    if dr != 0 and dc != 0:
        return None

    if dr > 0:
        return Direction.SOUTH
    if dr < 0:
        return Direction.NORTH
    if dc > 0:
        return Direction.EAST
    if dc < 0:
        return Direction.WEST

    return None

def direction_strict(start: Coordinate, target: Coordinate) -> Direction:
    """
    Returns the direction from start to target if one exists, raises exception otherwise
    """
    d = direction(start, target)
    if d is None:
        raise ValueError(f"{target} is not adiacent to {start}. Use direction() if adiacency is not guarantied")
    return d

def exit_direction(exit_cord: Coordinate, maze_size: int) -> Direction:
    """Return the direction where the maze exit is located, based on the target position."""
    exit_row, exit_col = exit_cord

    if exit_row == 0:
        return Direction.NORTH
    elif exit_row == maze_size - 1:
        return Direction.SOUTH
    elif exit_col == 0:
        return Direction.WEST
    elif exit_col == maze_size - 1:
        return Direction.EAST
    
    raise ValueError("Exit cell is not on the maze border")

def path_to_directions(path: list[Coordinate]) -> list[Direction]:
    """
    Convert a path (list of Coordinates) into a list of Directions.
    Each consecutive pair of coordinates must be adjacent.

    Args:
        path: List of coordinates forming a valid path.

    Returns:
        List of Directions representing the steps.

    Raises:
        ValueError: if two consecutive coordinates are not adjacent.
    """
    if len(path) < 2:
        return []

    directions: list[Direction] = []

    for a, b in zip(path, path[1:]):
        try:
            d = direction_strict(a, b)
        except ValueError:
            raise ValueError(
                f"Invalid path: coordinates {a} and {b} are not adjacent."
            ) from None

        directions.append(d)

    return directions

