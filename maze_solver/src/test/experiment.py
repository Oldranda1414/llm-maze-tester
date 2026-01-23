from experiment.run import run_experiment
from experiment.config import ExperimentConfig
from model.factory import random_model
from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.empty import EmptyStyle


def run() -> None:
    run_experiment(
        ExperimentConfig(
            [random_model()],
            PromptGenerator(EmptyStyle(), PromptConfig(True, True, 0, True)),
            [3],
            1,
            True,
            True,
        )
    )
