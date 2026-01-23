from maze import Maze
from maze.color.util import get_cell_color
from maze.core.direction import Direction
from prompt.facts import extract_facts
from prompt.style.narrative import NarrativeStyle
from prompt.style.narrative import prompts as narrative_prompts
from prompt.style.color import prompts
from prompt.util import length_to_string


class ColorStyle(NarrativeStyle):
    def preamble(
        self,
        maze: Maze,
        provide_legal_output_hint: bool,
        provide_spacial_awerness_hint: bool,
    ) -> str:
        preamble = super().preamble(
            maze, provide_legal_output_hint, provide_spacial_awerness_hint
        )
        return preamble + prompts.color_explanation

    def step_preamble(self, maze: Maze) -> str:
        position_cell_color = get_cell_color(maze.position, maze.colored_cells)
        if position_cell_color is None:
            return prompts.no_current_floor_color
        else:
            return prompts.current_floor_color.substitute(color=position_cell_color)

    def describe_direction(self, direction: Direction, maze: Maze) -> str:
        facts = extract_facts(direction, maze)
        base = narrative_prompts.direction.substitute(direction=str(direction))

        if facts.exit_distance and facts.exit_distance < maze.sight_depth:
            return base + narrative_prompts.exit_prompt

        if facts.is_exit:
            return base + narrative_prompts.exit_found

        if facts.is_wall:
            return base + narrative_prompts.wall

        if facts.out_of_sight:
            return (
                base
                + narrative_prompts.out_of_sight
                + super()._add_lateral_paths(facts)
            )

        # Visible corridor
        desc = base + narrative_prompts.corridor.substitute(
            path_length=length_to_string(facts.path_length)
        )

        if facts.is_dead_end:
            return desc + narrative_prompts.dead_end

        return desc + super()._add_lateral_paths(facts)
