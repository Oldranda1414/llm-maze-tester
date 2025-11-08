"""
A class that uses an LLM model to solve a maze.
"""
from typing import Any

from llm.model import Model
from llm.phony_model import Model as PhonyModel

from maze.factory import create_maze
from move import Direction

from prompt import step_prompt, illegal_answer_warning, illegal_direction_warning, get_preamble
from run import Run

class MazeSolver:
    """
    A class that uses an LLM model to solve a maze.
    The solver initializes a model and a maze, then prompts the model
    to make decisions about which direction to move at each step.
    """

    def __init__(self, model_name: str, maze_size: int = 6, sight_depth: int = 3, debug: bool = False):
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
        self.maze = create_maze(size=maze_size, sight_depth=sight_depth)
        self.debug = debug
        
        # Track last step errors
        self.invalid_answer_provided = False
        self.invalid_direction_provided = False

        # Statistics and tracking
        self.steps_taken = 0
        self.moves_history: list[str] = []
        self.visited_positions: set[tuple[int, int]] = set()
        self.is_solved = False
        self.position_history: list[tuple[int, int]] = []

        # Show the initial maze state
        self.maze.print()

    def step(self) -> dict[str, Any]:
        """
        Execute a single step in the maze solving process.
        
        Returns:
            A dictionary containing step results:
            - success: Whether the step was successful
            - move: The chosen move (if any)
            - position: The current position after the move
            - solved: Whether the maze is solved after this step
            - error: Error message if step failed
        """
        if self.is_solved:
            return {
                "success": False,
                "move": None,
                "position": self.maze.position(),
                "solved": True,
                "error": "Maze already solved"
            }

        available_directions = self.maze.get_directions()

        prompt = ""

        if self.steps_taken == 0:
            prompt += get_preamble(self.maze)
        if self.invalid_answer_provided:
            prompt += illegal_answer_warning(self.maze)
            self.invalid_answer_provided = False
        elif self.invalid_direction_provided:
            prompt += illegal_direction_warning(self.maze)
            self.invalid_direction_provided = False

        prompt += step_prompt(self.maze)

        response = self.model.ask(prompt)
        print(f"available_directions: {available_directions}")

        move = None
        decision = response[-1].upper()
        if decision in ["N", "S", "W", "E"]:
            if decision in [direction.to_coordinate() for direction in available_directions]:
                move = decision
            else:
                print(f"model provided an illegal direction: {decision}")
                self.invalid_direction_provided = True
        else:
            self.invalid_answer_provided = True

        if move is None:
            return {
                "success": False,
                "move": None,
                "position": self.maze.position(),
                "solved": False,
                "error": f"Invalid model response: '{response}'. Expected one of: {available_directions}"
            }

        current_position = self.maze.position()
        self.position_history.append(current_position)

        # Try to make the move and only record if valid
        try:
            valid_move = self.maze.move(Direction.from_coordinate(move))
            if valid_move:
                self.steps_taken += 1
                self.moves_history.append(move)
                new_position = self.maze.position()
                self.position_history.append(new_position)
                self.visited_positions.add(new_position)

                is_solved = self.maze.solved()
                if is_solved:
                    print(f"🎉 Maze solved in {self.steps_taken} steps!")
                    self.is_solved = True
                    self.maze.save("solved_maze.png")
                self.maze.print()

                return {
                    "success": True,
                    "move": move,
                    "position": new_position,
                    "solved": is_solved,
                    "steps_taken": self.steps_taken,
                }
            else:
                # Invalid move: do not record move or position
                return {
                    "success": False,
                    "move": move,
                    "position": self.maze.position(),
                    "solved": False,
                    "error": f"Invalid move '{move}': hit a wall."
                }

        except ValueError as e:
            return {
                "success": False,
                "move": move,
                "position": self.maze.position(),
                "solved": False,
                "error": f"Error executing move: {str(e)}"
            }

    def get_statistics(self) -> dict[str, Any]:
        """
        Get statistics about the maze solving progress.
        
        Returns:
            Dict with solving statistics
        """
        return {
            "steps_taken": self.steps_taken,
            "moves_history": self.moves_history,
            "is_solved": self.is_solved,
            "start_position": self.maze.start(),
            "end_position": self.maze.target(),
            "current_position": self.maze.position(),
            "maze_dimension": self.maze.size(),
            "unique_positions_visited": len(self.visited_positions)
        }

    def solved(self) -> bool:
        """
        Check if the maze is solved.
        
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self.is_solved

    def save_run(self, path: str) -> None:
        Run(self.maze, self.model.chat_history).save(path)

