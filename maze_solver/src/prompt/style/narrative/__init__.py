from maze import Maze
from maze.core.direction import Direction
from prompt.facts import Facts, extract_facts
from prompt.style import PromptStyle
from prompt.style.narrative import prompts
from prompt.style.narrative import warnings
from prompt.util import length_to_string


class NarrativeStyle(PromptStyle):
    def preamble(self, maze: Maze) -> str:
        return prompts.preamble.substitute(
            size=maze.size, sight_depth=length_to_string(maze.sight_depth)
        )

    def describe_direction(self, direction: Direction, maze: Maze) -> str:
        facts = extract_facts(direction, maze)
        base = prompts.direction.substitute(direction=str(direction))

        if facts.exit_distance and facts.exit_distance < maze.sight_depth:
            return base + prompts.exit_prompt

        if facts.is_exit:
            return base + prompts.exit_found

        if facts.is_wall:
            return base + prompts.wall

        # TODO this should consider laterla paths too
        if facts.out_of_sight:
            return base + prompts.out_of_sight + _add_lateral_paths(facts)

        # Visible corridor
        desc = base + prompts.corridor.substitute(
            path_length=length_to_string(facts.path_length)
        )

        if facts.is_dead_end:
            return desc + prompts.dead_end

        return desc + _add_lateral_paths(facts)

    def steps_summary(self, maze: Maze, steps_provided: int) -> str:
        """
        provides the last moves made in the maze
        if steps_provided == 0: all decisions are provided
        else: last steps_provided decisions are provided
        """
        print("steps_provided value:", steps_provided)
        # TODO this should not be decisions, this should actually be taken from path, as decisions contains moves made agianst walls also
        decisions = maze.decisions
        if len(decisions) == 0:
            return ""
        if steps_provided != 0:
            decisions = decisions[-steps_provided:]
        string_decisions = ", ".join(str(d) for d in decisions)
        return prompts.steps_summary.substitute(decisions=string_decisions)

    def step_epilogue(self) -> str:
        return prompts.step_epilogue

    def possible_moves(self, maze: Maze) -> str:
        directions = ", ".join(d.to_coordinate() for d in maze.available_directions())
        return prompts.possible_moves.substitute(directions=directions)

    def last_move_info(self, maze: Maze) -> str:
        return prompts.last_move.substitute(direction=maze.decisions[-1])

    def illegal_answer(self) -> str:
        return warnings.illegal_answer

    def illegal_direction(self, illegal_direction: str) -> str:
        return warnings.illegal_direction.substitute(direction=illegal_direction)


def _add_lateral_paths(facts: Facts) -> str:
    lateral_paths_description = ""
    if facts.lateral_paths is not None:
        for path in facts.lateral_paths:
            lateral_paths_description += prompts.lateral_path.substitute(
                direction=path.direction, distance=length_to_string(path.distance)
            )
    return (
        prompts.lateral_path_preable + lateral_paths_description
        if lateral_paths_description != ""
        else ""
    )
