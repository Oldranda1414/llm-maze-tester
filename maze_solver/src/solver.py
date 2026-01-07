"""
A class that uses an LLM model to solve a maze.
"""
from maze import Maze
from model import Model

from prompt import PromptGenerator
from run import Run
from util import extract_direction

class MazeSolver:
    """
    A class that uses an LLM model to solve a maze.
    The solver initializes a model and a maze, then prompts the model
    to make decisions about which direction to move at each step.
    """

    def __init__(self, model: Model, prompt_generator: PromptGenerator, maze: Maze, quiet: bool = False):
        self.prompt = prompt_generator
        self.maze = maze
        self.model = model
        system_prompt = prompt_generator.get_preamble(maze)
        model.set_system_prompt(system_prompt)
        self._quiet = quiet

        # Track last step errors
        self.invalid_answer_provided = False
        self.illegal_responses = 0
        self.invalid_direction_provided = False
        self.illegal_directions = 0
        self.valid_last_move = False

        # Show the initial maze state
        self._print_maze()

    def step(self, provide_history: bool = True) -> None:
        """
        Execute a single step in the maze solving process.
        """
        if self.maze.solved:
            raise RuntimeError("MazeSolver.step() called when maze solved. MazeSolver.step() cannot be called when maze is solved!")

        available_directions = self.maze.available_directions()

        step_prompt = ""

        if provide_history:
            if self.invalid_answer_provided:
                step_prompt += self.prompt.illegal_answer_warning()
                self.invalid_answer_provided = False
            elif self.invalid_direction_provided:
                step_prompt += self.prompt.illegal_direction_warning()
                self.invalid_direction_provided = False
            elif self.valid_last_move:
                step_prompt += self.prompt.last_move_info(self.maze)
        else:
            step_prompt += self.prompt.get_preamble(self.maze)

        step_prompt += self.prompt.step_prompt(self.maze)

        response = self.model.ask(step_prompt, provide_history)
        self._print_message(f"available_directions: {available_directions}")

        move = None
        decision = extract_direction(response)
        if decision:
            if decision in available_directions:
                move = decision
            else:
                self._print_message(f"model provided an illegal direction: {decision}")
                self.invalid_direction_provided = True
                self.illegal_directions += 1
        else:
            self.invalid_answer_provided = True
            self.illegal_responses += 1

        if move is None:
            return

        self.valid_last_move = self.maze.move(move)
        if self.valid_last_move:
            is_solved = self.maze.solved
            if is_solved:
                self._print_message(f"Maze solved!")
            self._print_maze()

    def is_solved(self) -> bool:
        """
        Check if the maze is solved.

        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self.maze.solved

    def save_run(self, path: str, execution_time: float) -> None:
        Run(self.maze, self.model.history, self.illegal_directions, self.illegal_responses, execution_time).save(path)

    def _print_maze(self):
        if not self._quiet:
            self.maze.print()

    def _print_message(self, message: str) -> None:
        if not self._quiet:
            print(message)

