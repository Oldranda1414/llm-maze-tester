from num2words import num2words

from maze import Maze
from maze.core.direction import Direction
from maze.core.navigation import neighbor


def path_length_str(direction: Direction, maze: Maze) -> str:
    return length_to_string(path_length(direction, maze))


def length_to_string(lenght: int) -> str:
    unit = "meter" if lenght == 1 else "meters"
    return f"{num2words(lenght)} {unit}"


def path_length(direction: Direction, maze: Maze) -> int:
    position = maze.position
    cl = maze.connection_list
    length = 0
    while cl.connected(position, n := neighbor(position, direction)):
        length += 1
        position = n
    return length


def exit_distance(maze):
    (px, py), (tx, ty) = maze.position, maze.target
    if px == tx:
        return abs(py - ty)
    if py == ty:
        return abs(px - tx)
    raise ValueError("Maze not axis-aligned for exit distance.")
