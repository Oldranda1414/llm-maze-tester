from experiment import Experiment
import sys


def main() -> None:
    if len(sys.argv) < 2:
        raise ValueError("No argument provided. Please provide the date of the experiment.")

    date = sys.argv[1]
    Experiment(date).print_experiment_stats()

if __name__ == "__main__":
    main()
