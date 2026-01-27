from copy import deepcopy
from maze import Maze
from maze.color.colored_cell import CellColor
from maze.color.util import get_cell_color
from maze.core.coordinate import Coordinate
from maze.core.direction import Direction
from prompt.facts import extract_facts
from prompt.style.narrative import NarrativeStyle
from prompt.style.narrative import prompts as narrative_prompts
from prompt.style.color import prompts
from prompt.util import length_to_string, path_length


class ColorStyle(NarrativeStyle):
    def preamble(
        self,
        maze: Maze,
        provide_legal_output_hint: bool,
        provide_spacial_awerness_hint: bool,
        provide_color_hint: bool,
        provide_repetition_hint: bool,
    ) -> str:
        preamble = super().preamble(
            maze,
            provide_legal_output_hint,
            provide_spacial_awerness_hint,
            provide_color_hint,
            provide_repetition_hint,
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

    def describe_color(self, direction: Direction, maze: Maze) -> str:
        maze = deepcopy(maze)
        path_len = path_length(direction, maze)
        desc: list[str] = [prompts.direction.substitute(direction=str(direction))]
        colored_cells_coordinates: list[Coordinate] = [
            cell.coordinate for cell in maze.colored_cells
        ]
        cell_colors: dict[Coordinate, CellColor] = {
            cell.coordinate: cell.color for cell in maze.colored_cells
        }

        for distance in range(1, min(path_len, maze.sight_depth) + 1):
            maze.move(direction)
            if maze.position in colored_cells_coordinates:
                color = cell_colors[maze.position]
                desc.append(
                    prompts.color_direction.substitute(
                        distance=length_to_string(distance), color=color
                    )
                )
        return "\n".join(desc) if len(desc) > 1 else ""
