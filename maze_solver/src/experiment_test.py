from experiment import run_experiment
from model.factory import phony_model

def main() -> None:
    run_experiment([phony_model("llama3")], [3], 1, True)

if __name__ == "__main__":
    main()

