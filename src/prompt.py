from maze import Direction, Maze

def generate_prompt(maze: Maze) -> str: 
    paths: dict[Direction, int]  = {}
    directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    initial_position = maze.position()
    original_path = maze.path()
    for direction in directions:
        counter = 0
        while direction in maze.get_directions():
            counter += 1
            maze.move(direction)
        paths[direction] = counter
        maze.set_position(initial_position)
    maze.set_path(original_path)

    return str(paths)
