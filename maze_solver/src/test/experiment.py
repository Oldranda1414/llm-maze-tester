from experiment import run_experiment
from experiment.config import ExperimentConfig
from model.factory import random_model

def run() -> None:
    run_experiment(ExperimentConfig([random_model("llama3")], [3], 1, True))

