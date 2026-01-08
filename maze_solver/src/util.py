import re

from chat_history import Exchange
from maze import Maze
from maze.core.direction import Direction


def seconds_to_padded_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = round(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


def format_float(value: float) -> str:
    return f"{value:.2f}"


def extract_direction(response: str) -> Direction | None:
    if not response:
        return None

    # Matches either:
    #  - single-letter coordinates: N S E W
    #  - full words: north south east west
    #
    # Ensures they are delimited by whitespace or punctuation
    pattern = re.compile(
        r"""
        (?<!\w)                    # not preceded by a word char
        (
            N|S|E|W
            |north|south|east|west
        )
        (?!\w)                     # not followed by a word char
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    matches = list(pattern.finditer(response))
    if not matches:
        return None

    last = matches[-1].group(1).lower()

    # Normalize to Direction
    if last in {"n", "north"}:
        return Direction.NORTH
    if last in {"e", "east"}:
        return Direction.EAST
    if last in {"s", "south"}:
        return Direction.SOUTH
    if last in {"w", "west"}:
        return Direction.WEST

    return None


def execute_history(
    maze: Maze, chat: list[Exchange], step_index: int | None = None
) -> Maze:
    if step_index is None:
        step_index = len(chat)
    maze.reset()
    for i in range(step_index):
        response = extract_direction(chat[i].response)
        if response is not None:
            next_move = response
            maze.move(next_move)
    return maze
