from maze import Maze
from maze.core.direction import Direction
from prompt.facts import extract
from prompt.style import PromptStyle
from prompt.style.narrative import prompts
from prompt.style.narrative import warnings
from prompt.util import length_to_string

class NarrativeStyle(PromptStyle):

    def preamble(self, maze: Maze):
        return prompts.preamble.substitute(size=maze.size)

    def response_rules(self) -> str:
        return prompts.response_rules

    def strategy_hint(self) -> str:
        return prompts.strategy_hint

    def describe_direction(self, direction: Direction, maze: Maze) -> str:

        facts = extract(direction, maze)

        base = prompts.direction.substitute(direction=str(direction))

        if facts.exit_distance and facts.exit_distance < maze.sight_depth:
            return base + prompts.exit_prompt

        if facts.is_exit:
            return base + prompts.exit_found

        if facts.is_wall:
            return base + prompts.wall

        if facts.out_of_sight:
            return base + prompts.out_of_sight

        # Visible corridor
        desc = base + prompts.corridor.substitute(path_length=length_to_string(facts.path_length))

        if facts.is_dead_end:
            return desc + prompts.dead_end

        return desc + prompts.options

    def steps_summary(self, maze: Maze):
        decisions = maze.decisions
        if len(decisions) == 0:
            return ""
        string_decisions = ", ".join(str(d) for d in decisions)
        return prompts.steps_summary.substitute(decisions=string_decisions)

    def step_epilogue(self, maze: Maze):
        directions = ", ".join(d.to_coordinate() for d in maze.available_directions())
        return prompts.step_epilogue.substitute(directions=directions)

    def last_move_info(self, maze: Maze) -> str:
        return prompts.last_move.substitute(direction=maze.decisions[-1])  

    def illegal_answer(self) -> str:
        return warnings.illegal_answer

    def illegal_direction(self) -> str:
        return warnings.illegal_direction

