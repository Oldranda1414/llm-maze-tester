from num2words import num2words

from maze import Coordinate, Direction, Maze

def generate_step_prompt(maze: Maze) -> str: 
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    initial_position = maze.position()
    original_path = maze.path()
    step_prompt = ""
    for direction in directions:
        step_prompt += get_path_prompt(direction, maze, initial_position) + "\n"
    maze.set_path(original_path)

    return step_prompt

def get_path_prompt(direction: Direction, maze: Maze, initial_position: Coordinate) -> str:
    path_lenght = get_path_length(direction, maze, initial_position)
    prompt = f"Due {str(direction)} there is "
    if path_lenght == 0:
        return prompt + "a wall."
    path_lenght_word = num2words(path_lenght)
    return prompt + f"a corridor that goes on for {path_lenght_word} meters before encountering a wall."

def get_path_length(direction: Direction, maze: Maze, initial_position: Coordinate) -> int:
    counter = 0
    while direction in maze.get_directions():
        counter += 1
        maze.move(direction)
    maze.set_position(initial_position)
    return counter
    
