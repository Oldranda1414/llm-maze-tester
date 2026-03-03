from typing import Any, cast
import matplotlib.pyplot as plt
from maze import Maze
from maze.lattice_maze import LatticeMaze
from maze.output import draw_maze
from experiment import Experiment


def maze_exp_example(path: str):
    maze_config = [
        {"date": "2026-01-12_14:15:25", "index": 0},
        {"date": "2026-03-02_14:41:15", "index": 6},
    ]

    mazes = get_mazes(maze_config)
    _, axes = plt.subplots(1, 2, figsize=(12, 6))

    for idx, maze in enumerate(mazes):
        draw_maze(maze, ax=axes[idx], draw_character=True, highlight_seen_tiles=False)

    plt.tight_layout()
    plt.savefig(f"{path}/maze_exp_example.png", bbox_inches="tight", dpi=150)


def get_mazes(maze_config: list[dict[str, Any]]) -> list[Maze]:
    mazes: list[Maze] = []

    for config in maze_config:
        experiment = Experiment(config["date"])
        first_run = next(iter(experiment.runs.values()), None)

        if first_run is None:
            print(f"No runs found for experiment {config['date']}")
            continue

        if not first_run:
            print(f"Run exists but is empty for experiment {config['date']}")
            continue

        maze = first_run[config["index"]].maze
        maze = cast(LatticeMaze, maze)
        maze._colored_cells = []
        mazes.append(maze)

    return mazes
