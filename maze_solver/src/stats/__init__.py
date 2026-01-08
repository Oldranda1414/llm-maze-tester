import sys
from typing import Callable

from experiment import Experiment, experiment_list
from stats.experiment import print_experiment_stats
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
    for date in dates:
        if date not in experiment_list():
            print(f"Provided date ({date}) is not a valid experiment date")
            print_experiment_list()
            return
        print_experiment_stats(Experiment(date), STATS)


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
