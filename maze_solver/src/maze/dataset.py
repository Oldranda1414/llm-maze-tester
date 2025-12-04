import random
from typing import Callable

from maze_dataset import MazeDataset as DatasetMazeDataset, MazeDatasetConfig
from maze_dataset.generation import LatticeMazeGenerators

from maze import Maze, generate_start, generate_target
from maze.core.connection_list import ConnectionList
from maze.lattice_maze import LatticeMaze


class MazeDataset:

    def __init__(
        self,
        name: str,
        n_mazes: int,
        maze_size: int,
        sight_depth: int,
        seed: int,
        maze_filter: Callable[[Maze], bool] | None = None,
        attempts: int = 100,
    ):

        config = MazeDatasetConfig(
            name=name,
            grid_n=maze_size,
            n_mazes=n_mazes,
            maze_ctor=LatticeMazeGenerators.gen_dfs,
            seed=seed,
        )
        dataset = DatasetMazeDataset.from_config(config)

        self.mazes: list[Maze] = []
        rng = random.Random(seed)

        for d_maze in dataset.mazes:
            if not maze_filter:
                self.mazes.append(_generate_maze(d_maze, rng, sight_depth))
            else:
                for _ in range(attempts):
                    maze = _generate_maze(d_maze, rng, sight_depth)
                    if maze_filter(maze):
                        self.mazes.append(maze)
                        break
                else:
                    raise RuntimeError(
                        f"Failed to generate a valid maze after {attempts} attempts."
                    )

def _generate_maze(d_maze: DatasetMazeDataset, rng: random.Random, sight_depth: int) -> Maze:
        maze_size = d_maze.grid_n
        target = generate_target(maze_size, rng=rng)
        start = generate_start(maze_size, target, rng=rng)
        return LatticeMaze(
            ConnectionList(
                d_maze.connection_list[0].tolist(),
                d_maze.connection_list[1].tolist(),
            ),
            maze_size,
            start,
            target,
            sight_depth,
        )

