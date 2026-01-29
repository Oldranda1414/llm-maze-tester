from maze import Maze
from maze.core.direction import Direction
from prompt.style import PromptStyle


class EmptyStyle(PromptStyle):
    def preamble(
        self,
        maze: Maze,
        provide_legal_output_hint: bool,
        provide_spacial_awerness_hint: bool,
        provide_color_hint: bool,
        provide_repetition_hint: bool,
    ) -> str:
        _ = maze
        _ = provide_legal_output_hint
        _ = provide_spacial_awerness_hint
        _ = provide_color_hint
        _ = provide_repetition_hint
        return ""

    def step_preamble(self, maze: Maze) -> str:
        _ = maze
        return ""

    def describe_direction(self, direction: Direction, maze: Maze) -> str:
        _ = direction
        _ = maze
        return ""

    def describe_color(self, direction: Direction, maze: Maze) -> str:
        _ = direction
        _ = maze
        return ""

    def step_epilogue(self) -> str:
        return ""

    def steps_summary(self, maze: Maze, steps_provided: int | None = None) -> str:
        _ = maze
        _ = steps_provided
        return ""

    def last_move_info(self, maze: Maze) -> str:
        _ = maze
        return ""

    def possible_moves(self, maze: Maze) -> str:
        _ = maze
        return ""

    def illegal_answer(self) -> str:
        return ""

    def illegal_direction(self, illegal_direction: str) -> str:
        _ = illegal_direction
        return ""

    def cot_reminder(self) -> str:
        return ""
