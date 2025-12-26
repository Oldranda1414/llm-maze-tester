from experiment import run_experiment
from model.factory import random_model

def main() -> None:
    run_experiment([random_model("llama3")], [3], 1)

if __name__ == "__main__":
    main()

