from maze import Maze

if __name__ == "__main__":
    m = Maze()

    print("Start:", m.start)
    print("End:", m.end)
    print("Initial position:", m.position())
    m.print()

    print("Available directions:", m.get_directions())

    m.move("R")
    print("New position:", m.position())
    print("Solved?", m.solved())

