import re

from chat_history import Exchange
from maze import Maze
from maze.core.direction import Direction

def seconds_to_padded_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = round(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

def extract_direction(response: str) -> str | None:
    if not response:
        return None

    # Look for a single direction letter at the end (optionally wrapped in punctuation)
    match = re.search(r"\b([NSEW])\b\s*$", response.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()

    return None

def set_path(maze: Maze, chat: list[Exchange], step_index: int | None = None) -> Maze:
    if not step_index:
        step_index = len(chat)
    maze.reset()
    for i in range(step_index):
        response = extract_direction(chat[i].response)
        if response in ["W","N","E","S"]:
            next_move = Direction.from_coordinate(response)
            maze.move(next_move)
    return maze

