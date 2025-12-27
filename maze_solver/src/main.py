from experiment import run_experiment
from experiment.config import ExperimentConfig

def main():
    config_path = "experiment_config.yaml"
    config = ExperimentConfig.from_yaml(config_path)
    run_experiment(config)


if __name__ == "__main__":
    main()

