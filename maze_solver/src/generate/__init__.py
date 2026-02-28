from generate.lateral_path import lateral_path
from generate.prompt_step_example import prompt_step_example
from generate.prompt_example import prompt_example
from generate.sight_depth import sight_depth
from generate.colored_example import colored_example
from generate.selection_example import selection_example

FIGURES_PATH = "./figures"


def main():
    colored_example(FIGURES_PATH)
    selection_example(FIGURES_PATH)
    sight_depth(FIGURES_PATH)
    lateral_path(FIGURES_PATH)
    prompt_step_example(FIGURES_PATH)
    prompt_example(FIGURES_PATH)
