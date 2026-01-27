from maze import Maze
from maze.core.direction import Direction
from prompt.config import PromptConfig
from prompt.style import PromptStyle


class PromptGenerator:
    def __init__(self, style: PromptStyle, config: PromptConfig):
        self.style = style
        self.config = config

    def get_preamble(self, maze: Maze) -> str:
        return self.style.preamble(
            maze,
            self.config.provide_legal_output_hint,
            self.config.provide_spacial_awerness_hint,
            self.config.provide_color_hint,
            self.config.provide_repetition_hint,
        )

    def step_prompt(self, maze: Maze) -> str:
        parts = [self.style.step_preamble(maze)]
        for direction in Direction:
            parts.append(self.style.describe_direction(direction, maze))

        step_prompt = "\n".join(parts)
        color_parts: list[str] = []
        for direction in Direction:
            color_desc = self.style.describe_color(direction, maze)
            if len(color_desc) > 0:
                color_parts.append(color_desc)
        if len(color_parts) > 0:
            step_prompt += "\n\n" + "\n".join(color_parts)

        if self.config.provide_steps_summary is not None:
            step_prompt += self.style.steps_summary(
                maze, self.config.provide_steps_summary
            )
        if self.config.provide_possible_moves:
            step_prompt += self.style.possible_moves(maze)
        return step_prompt

    def last_move_info(self, maze: Maze) -> str:
        return self.style.last_move_info(maze)

    def illegal_answer_warning(self) -> str:
        return self.style.illegal_answer()

    def illegal_direction_warning(self, illegal_direction: str) -> str:
        return self.style.illegal_direction(illegal_direction)
