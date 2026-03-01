import sys
from typing import Callable

from experiment import Experiment, experiment_list
from run.git import current_hash
from stats.output import print_experiment_stats
from stats.stats import STATS


def help():
    print("If first argument is not a command, it must be a valid experiment date")
    print("Possible commands:")
    print("   last: print stats of last experiment")
    print("   list: list available experiment dates")
    print("   help: print help message")


def last():
    default([experiment_list()[-1]])


def print_experiment_list():
    print("Available experiments:")
    print("\n".join(experiment_list()))


def default(dates: list[str]):
    if len(dates) == 1:
        date = dates[0]
        if date not in experiment_list():
            print(f"Provided date ({date}) is not a valid experiment date")
            print_experiment_list()
            return
        print(f"Loading experiment in date {date}")
        experiment = Experiment(date)
        git_hash = current_hash()
        experiment_git_hash = experiment.git_hash
        if experiment_git_hash and git_hash != experiment_git_hash:
            print(
                f"The current commit ({git_hash}) is not the same the experiment was run on ({experiment_git_hash}) "
            )
            print(
                f"To ensure correct stats display, run 'git checkout {experiment_git_hash}'"
            )
        print_experiment_stats(experiment, STATS)
    else:
        print("Provide one and only one valid experiment date to print stats")
        help()


def commands() -> dict[str, Callable]:
    return {"help": help, "last": last, "list": print_experiment_list}


def main() -> None:
    if len(sys.argv) == 1:
        help()
        return

    args = sys.argv[1:]
    if len(args) == 1 and args[0] in commands().keys():
        commands()[args[0]]()
    else:
        default(args)
