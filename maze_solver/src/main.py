from experiment import Experiment

def main():
    model_names = ["llama3"]
    maze_sizes = [3,4,5,6]
    iterations = 10
    experiment = Experiment(model_names, maze_sizes, iterations)
    experiment.run()

if __name__ == "__main__":
    main()
