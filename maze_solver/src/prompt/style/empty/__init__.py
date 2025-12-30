from maze import Maze
from maze.core.direction import Direction
from prompt.style import PromptStyle

class EmptyStyle(PromptStyle):

    def preamble(self, maze: Maze) -> str:
        _ = maze
        return ""

    def describe_direction(self, direction: Direction, maze: Maze) -> str:
        _ = direction
        _ = maze
        return ""

    def step_epilogue(self, maze: Maze) -> str:
        _ = maze
        return ""

    def steps_summary(self, maze: Maze) -> str:
        _ = maze
        return ""

    def last_move_info(self, maze: Maze) -> str:
        _ = maze
        return ""

    def illegal_answer(self) -> str:
        return ""

    def illegal_direction(self) -> str:
        return ""
