"""
A class that uses an LLM model to solve a maze.
"""
from typing import Any

from llm.model import Model
from llm.phony_model import Model as PhonyModel

from maze.factory import create_maze
from maze.core.direction import Direction

from prompt import PromptGenerator
from prompt.style import PromptStyle
from run import Run

class MazeSolver:
    """
    A class that uses an LLM model to solve a maze.
    The solver initializes a model and a maze, then prompts the model
    to make decisions about which direction to move at each step.
    """

    def __init__(self, model_name: str, prompt_style: PromptStyle, maze_size: int = 6, sight_depth: int = 3, seed: int = 42, debug: bool = False, quiet: bool = False):
        """
        Initialize the maze solver with a model and maze.
        
        Args:
            model_name: Name of the LLM model to use
            maze_size: Width and height of the maze
        """
        if debug:
            self.model = PhonyModel(model_name)
        else:
            self.model = Model(model_name)
        self.prompt = PromptGenerator(prompt_style)
        self.maze = create_maze(size=maze_size, sight_depth=sight_depth, seed=seed)
        self.debug = debug
        self._quiet = quiet
        
        # Track last step errors
        self.first_step = True
        self.invalid_answer_provided = False
        self.illegal_responses = 0
        self.invalid_direction_provided = False
        self.illegal_directions = 0
        self.valid_last_move = False

        # Statistics and tracking
        self.steps_taken = 0

        # Show the initial maze state
        self._print_maze()

    def step(self, provide_history: bool = True) -> None:
        """
        Execute a single step in the maze solving process.
        """
        available_directions = self.maze.available_directions()

        step_prompt = ""

        if provide_history:
            if self.first_step:
                self.first_step = False
                step_prompt += self.prompt.get_preamble(self.maze)
            elif self.invalid_answer_provided:
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
        decision = response[-1].upper()
        if decision in ["N", "S", "W", "E"]:
            if decision in [direction.to_coordinate() for direction in available_directions]:
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

        self.valid_last_move = self.maze.move(Direction.from_coordinate(move))
        if self.valid_last_move:
            self.steps_taken += 1

            is_solved = self.maze.solved
            if is_solved:
                self._print_message(f"🎉 Maze solved in {self.steps_taken} steps!")
                self.maze.save("solved_maze.png")
            self._print_maze()

    def get_statistics(self) -> dict[str, Any]:
        """
        Get statistics about the maze solving progress.
        
        Returns:
            Dict with statistics
        """
        return {
            "steps_taken": self.steps_taken,
            "moves_history": self.maze.decisions,
            "is_solved": self.is_solved(),
            "start_position": self.maze.start,
            "end_position": self.maze.target,
            "current_position": self.maze.position,
            "maze_dimension": self.maze.size,
            "unique_positions_visited": len(set(self.maze.path)),
            "illegal_directions": self.illegal_directions,
            "illegal_responses": self.illegal_responses,
        }

    def is_solved(self) -> bool:
        """
        Check if the maze is solved.
        
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self.maze.solved

    def save_run(self, path: str, execution_time: float) -> None:
        Run(self.maze, self.model.chat_history, self.illegal_directions, self.illegal_responses, execution_time).save(path)

    def _print_maze(self):
        if not self._quiet:
            self.maze.print()

    def _print_message(self, message: str) -> None:
        if not self._quiet:
            print(message)
