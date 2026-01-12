import sys
import os

from run import Run
from run.render import run_to_mp4


def main() -> None:
    args = sys.argv[1:]

    if len(args) == 0 or len(args) > 2:
        print("Usage:")
        print("     just render <path-to-run> [output-file]")
        return

    run_path = args[0]
    if not os.path.exists(run_path):
        print(f"[Error]   No file exists at {run_path}")
        return

    run = Run.load(args[0])
    if len(args) == 1:
        run_to_mp4(run)
    elif len(args) == 2:
        run_to_mp4(run, args[1])
