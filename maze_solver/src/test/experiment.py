from experiment import run_experiment
from experiment.config import ExperimentConfig
from model.factory import random_model
from prompt import PromptGenerator
from prompt.style.empty import EmptyStyle

def run() -> None:
    run_experiment(ExperimentConfig([random_model("llama3")], PromptGenerator(EmptyStyle()), [3], 1, True, True))

