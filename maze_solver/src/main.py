from experiment import run_experiment

def main():
    model_names = ["llama3"]
    maze_sizes = [3,4,5,6]
    iterations = 10
    run_experiment(model_names, maze_sizes, iterations)

if __name__ == "__main__":
    main()
