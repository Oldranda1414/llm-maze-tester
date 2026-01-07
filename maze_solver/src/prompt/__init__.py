from maze import Maze
from maze.core.direction import Direction
from prompt.style import PromptStyle

class PromptGenerator:

    def __init__(self, style: PromptStyle):
        self.style = style

    def get_preamble(self, maze: Maze) -> str:
        return self.style.preamble(maze) + self.style.response_rules()

    def step_prompt(self, maze: Maze) -> str:
        parts = []
        for direction in Direction:
            parts.append(self.style.describe_direction(direction, maze))

        return (
            "\n".join(parts)
            + "\n\n"
            + self.style.steps_summary(maze)
            + self.style.step_epilogue(maze)
            + self.style.strategy_hint()
            + self.style.response_rules()
        )

    def last_move_info(self, maze: Maze) -> str:
        return self.style.last_move_info(maze)

    def illegal_answer_warning(self) -> str:
        return self.style.illegal_answer()

    def illegal_direction_warning(self) -> str:
        return self.style.illegal_direction()

