from maze.core.direction import Direction
from maze.factory import create_maze, create_dataset
from prompt import PromptGenerator
from prompt.config import PromptConfig
from prompt.style.narrative import NarrativeStyle


def run():
    maze_size = 3
    sight_depth = 3
    maze = create_maze(size=maze_size, sight_depth=sight_depth)
    pg = PromptGenerator(NarrativeStyle(), PromptConfig(True, True, 0, True))
    print(pg.get_preamble(maze))

    while not maze.solved:
        print(pg.step_prompt(maze))
        maze.print()

        move = input("give me a move (C to close): ")
        move = move.strip(" ").upper()
        while move not in ["N", "E", "S", "W", "C"]:
            print("invalid move try again")
            move = input("give me a move (C to close): ")
            move = move.strip(" ").upper()

        if move == "C":
            break

        maze.move(Direction.from_coordinate(move))
        print("New position:", maze.position)
        print("Solved?", maze.solved)


def many_maze():
    sight_depth = 3
    mazes = create_dataset(10, 3, sight_depth).mazes
    pg = PromptGenerator(NarrativeStyle(), PromptConfig(False, False, None, False))
    for maze in mazes:
        print(pg.get_preamble(maze))

        while not maze.solved:
            print(pg.step_prompt(maze))
            maze.print()

            move = input("give me a move (C to close): ")
            move = move.strip(" ").upper()
            while move not in ["N", "E", "S", "W", "C"]:
                print("invalid move try again")
                move = input("give me a move (C to close): ")
                move = move.strip(" ").upper()

            if move == "C":
                break

            maze.move(Direction.from_coordinate(move))
            print("New position:", maze.position)
            print("Solved?", maze.solved)
