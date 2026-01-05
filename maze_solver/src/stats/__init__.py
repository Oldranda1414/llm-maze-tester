import sys
import os
from typing import Callable

from experiment import Experiment

def help():
    print("If first argument is not a command, it must be a valid experiment date")
    print("Possible commands:")
    print("   last: print stats of last experiment")
    print("   list: list available experiment dates")
    print("   help: print help message")

def last():
    default([experiment_list()[-1]])

def print_experiment_list():
    print('Available experiments:')
    print("\n".join(experiment_list()))

def default(dates: list[str]):
    for date in dates:
        if date not in experiment_list():
            print(f"Provided date ({date}) is not a valid experiment date")
            print_experiment_list()
            return
        Experiment(date).print_experiment_stats()

def commands() -> dict[str, Callable]:
    return {
        "help": help,
        "last": last,
        "list": print_experiment_list
    }

def experiment_list():
    experiments = [d for d in os.listdir('results') if os.path.isdir(os.path.join('results', d))]
    experiments.remove("logs")
    experiments.sort()
    return experiments if experiments else []

def main() -> None:
    if len(sys.argv) == 1:
        help()
        return

    args = sys.argv[1:]
    if len(args) == 1 and args[0] in commands().keys():
        commands()[args[0]]()
    else:
        default(args)

