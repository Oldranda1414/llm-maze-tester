import subprocess
from pathlib import Path
from typing import Callable

from experiment import Experiment, experiment_list
from stats.output import print_experiment_stats
from stats.stats import STATS

LOG_PATH = "exp_log"


def run() -> None:
    print("starts")
    e_list = load_experiments()
    print("loaded experiments")
    for experiment in e_list:
        path = log_path(experiment.date)
        with open(path, "a", encoding="utf-8") as f:
            print_fn = get_print_fn(f)
            try:
                config = get_config(experiment)
                if config:
                    print_fn(f"git_hash:{experiment.git_hash}\n")
                    print_fn("--------STATS---------")
                    print_experiment_stats(experiment, STATS, print_fn, False)
                    print_fn("--------CONFIG---------")
                    print_fn(config)
            except Exception as e:
                print_fn("exception occurred")
                print_fn(f"Error: {e}")


def load_experiments() -> list[Experiment]:
    failed_loades = []
    e_name_list = experiment_list()
    e_list = []
    for experiment_date in e_name_list:
        try:
            experiment = Experiment(experiment_date)
            e_list.append(experiment)
        except Exception as e:
            print("could not load experiment:", experiment_date)
            print(f"Error: {e}")
            failed_loades.append(experiment_date)
    print("experiments not loaded:", ",".join(failed_loades))
    return e_list


def get_print_fn(f) -> Callable[[str], None]:
    def print_fn(line: str) -> None:
        f.write(line + "\n")

    return print_fn


def log_path(experiment_date: str) -> str:
    return f"{LOG_PATH}/{experiment_date}"


def get_config(experiment: Experiment) -> str | None:
    clone_path = "../../../../temp_clone/llm-maze-tester"
    script_dir = Path(__file__).resolve().parent
    workdir = script_dir / clone_path

    git_path = "maze_solver/src/experiment/config.py"

    result = subprocess.run(
        ["git", "show", f"{experiment.git_hash}:{git_path}"],
        cwd=workdir,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        return result.stdout

    return None
