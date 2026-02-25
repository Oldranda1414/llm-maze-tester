from maze.factory import create_maze


def lateral_path(path: str):
    maze_size = 5
    maze = create_maze(maze_size)
    maze.save(f"{path}/lateral_path.png", True, True)
