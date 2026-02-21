from maze import Maze
from maze.color.util import get_cell_color
from maze.core.direction import Direction
from prompt.facts import Facts, extract_facts
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
        provide_color_hint: bool,
        provide_repetition_hint: bool,
        provide_avoid_dead_end: bool,
    ) -> str:
        preamble = super().preamble(
            maze,
            provide_legal_output_hint,
            provide_spacial_awerness_hint,
            provide_color_hint,
            provide_repetition_hint,
            provide_avoid_dead_end,
        )
        return preamble + prompts.color_explanation if provide_color_hint else preamble

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
            additional_info = (
                prompts.additional_direction_info + self._add_dir_info(facts)
                if self._add_dir_info(facts) != ""
                else ""
            )
            return base + narrative_prompts.out_of_sight + additional_info

        # Visible corridor
        desc = base + narrative_prompts.corridor.substitute(
            path_length=length_to_string(facts.path_length)
        )

        if facts.is_dead_end:
            return desc + narrative_prompts.dead_end

        additional_info = (
            prompts.additional_direction_info + self._add_dir_info(facts)
            if self._add_dir_info(facts) != ""
            else ""
        )
        return desc + additional_info

    def _add_dir_info(self, facts: Facts) -> str:
        lateral_paths = super()._add_lateral_paths(facts)
        floors_info = [""]
        if facts.colored_floors is not None:
            for colored_floor in facts.colored_floors:
                floors_info.append(
                    prompts.color_direction.substitute(
                        distance=length_to_string(colored_floor.distance),
                        color=colored_floor.color,
                    )
                )
        return (
            lateral_paths + "\n".join(floors_info)
            if len(floors_info) > 1
            else lateral_paths
        )
