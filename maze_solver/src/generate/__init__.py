from generate.colored_example_less import colored_example_less
from generate.lateral_path import lateral_path
from generate.prompt_step_example import prompt_step_example
from generate.prompt_example import prompt_example
from generate.sight_depth import sight_depth
from generate.colored_example import colored_example
from generate.selection_example import selection_example
from generate.selection_example_flipped import selection_example_flipped
from generate.maze_exp_example import maze_exp_example
from generate.task_example import task_example
from generate.sight_depth_flipped import sight_depth_flipped
from generate.prompt_step_example_plus import prompt_step_example_plus
from generate.prompt_example_plus import prompt_example_plus
from generate.maze_exp_example_plus import maze_exp_example_plus

FIGURES_PATH = "./figures"


def main():
    colored_example(FIGURES_PATH)
    selection_example(FIGURES_PATH)
    sight_depth(FIGURES_PATH)
    lateral_path(FIGURES_PATH)
    prompt_step_example(FIGURES_PATH)
    prompt_example(FIGURES_PATH)
    maze_exp_example(FIGURES_PATH)
    task_example(FIGURES_PATH)
    selection_example_flipped(FIGURES_PATH)
    colored_example_less(FIGURES_PATH)
    sight_depth_flipped(FIGURES_PATH)
    prompt_step_example_plus(FIGURES_PATH)
    prompt_example_plus(FIGURES_PATH)
    maze_exp_example_plus(FIGURES_PATH)
