from experiment.run import run_experiment
from experiment.config import load_config


def main():
    run_experiment(load_config())


if __name__ == "__main__":
    main()
