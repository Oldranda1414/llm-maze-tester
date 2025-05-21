from maze import Maze

if __name__ == "__main__":
    # m = Maze(plot=False)
    m = Maze(block_on_plot=False)

    print("Start:", m.start)
    print("End:", m.end)
    print("Initial position:", m.position())

    while not m.solved():

        m.print()

        print("Available directions:", m.get_directions())

        move = input("give me a move (C to close): ")
        move = move.strip(" ").upper()
        while move not in ["U","D","L","R", "C"]:
            print("invalid move try again")
            move = input("give me a move (C to close): ")

        if move == "C":
            break

        m.move(move)
        print("New position:", m.position())
        print("Solved?", m.solved())

    input("press any button to exit")

