from collections import defaultdict
import os

from run import Run


class Experiment:
    def __init__(self, date: str):
        base_path = "results"
        experiment_path = os.path.join(base_path, date)

        self.date: str = date
        self.git_hash: str | None = None
        self.runs: dict[str, list[Run]] = defaultdict(list)

        for root, _, files in os.walk(experiment_path):
            for file in files:
                if not file.endswith(".yaml"):
                    continue

                file_path = os.path.join(root, file)

                # Get path relative to the experiment directory
                rel_path = os.path.relpath(root, experiment_path)
                parts = rel_path.split(os.sep)

                # Expect: <model>/<maze_dim>/<i>.yaml
                if not parts or parts[0] == ".":
                    continue

                model_name = parts[0]

                run = Run.load(file_path)
                if self.git_hash is None:
                    self.git_hash = run.git_hash
                self.runs[model_name].append(run)


def experiment_list() -> list[str]:
    experiments = [
        d for d in os.listdir("results") if os.path.isdir(os.path.join("results", d))
    ]
    experiments.remove("logs")
    experiments.sort()
    return experiments if experiments else []
