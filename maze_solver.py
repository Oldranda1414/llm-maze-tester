"""
maze_solver.py
A class that uses an LLM model to solve a maze.
"""
from typing import Dict, Any, List

from model import Model
from maze import Maze

class MazeSolver:
    """
    A class that uses an LLM model to solve a maze.
    The solver initializes a model and a maze, then prompts the model
    to make decisions about which direction to move at each step.
    """

    # Template for the initial prompt to the model
    INITIAL_PROMPT = """
        You are a maze-solving AI.
        Your task is to navigate through a {width}x{height} maze from the starting point to the endpoint.

        You are currently at position {start_pos}.
        The end goal is at position {end_pos}.

        For each step, I will tell you your current position, the goal position, and which moves are available.
        You must respond with ONLY a single letter representing your chosen direction:
        - U (up)
        - D (down)
        - L (left)
        - R (right)

        Do not provide any explanation, just respond with a single letter U, D, L, or R.
    """

    # Template for each step's prompt
    STEP_PROMPT = """
        Current position: {current_pos}
        Goal position: {end_pos}
        Available moves: {available_moves}

        Choose your next move (respond with only a single letter: {move_options}):
    """

    def __init__(self, model_name: str, maze_width: int = 6, maze_height: int = 6,
                 plot: bool = True, block_on_plot: bool = False):
        """
        Initialize the maze solver with a model and maze.
        
        Args:
            model_name: Name of the LLM model to use
            maze_width: Width of the maze
            maze_height: Height of the maze
            plot: Whether to display the maze graphically
            block_on_plot: Whether to block execution when showing plots
        """
        # Initialize the model
        print(f"Initializing model '{model_name}'...")
        self.model = Model(model_name)

        # Initialize the maze
        print(f"Creating {maze_width}x{maze_height} maze...")
        self.maze = Maze(width=maze_width, height=maze_height,
                        plot=plot, block_on_plot=block_on_plot)

        # Statistics and tracking
        self.steps_taken = 0
        self.moves_history: List[str] = []
        self.is_solved = False

        # Initial briefing to the model
        self._send_initial_prompt()

        # Show the initial maze state
        self.maze.print()

    def _send_initial_prompt(self) -> None:
        """Send the initial prompt to the model explaining its task."""
        initial_prompt = self.INITIAL_PROMPT.format(
            width=self.maze.width,
            height=self.maze.height,
            start_pos=self.maze.position(),
            end_pos=self.maze.end
        )

        # Send the initial prompt to the model
        response = self.model.ask(initial_prompt)
        print(f"Model initialized for maze solving. Initial response: {response}")

    def step(self) -> Dict[str, Any]:
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
        # If already solved, just return
        if self.is_solved:
            return {
                "success": False,
                "move": None,
                "position": self.maze.position(),
                "solved": True,
                "error": "Maze already solved"
            }

        # Get available directions
        available_directions = self.maze.get_directions()

        # Construct the prompt for this step
        prompt = self.STEP_PROMPT.format(
            current_pos=self.maze.position(),
            end_pos=self.maze.end,
            available_moves=", ".join(available_directions),
            move_options=", ".join(available_directions)
        )

        # Ask the model for the next move
        response = self.model.ask(prompt)
        print(f"Model response: {response}")

        # Parse the response (extract first valid direction)
        move = None
        for char in response:
            if char.upper() in ["U", "D", "L", "R"] and char.upper() in available_directions:
                move = char.upper()
                break

        # Handle invalid response
        if move is None:
            return {
                "success": False,
                "move": None,
                "position": self.maze.position(),
                "solved": False,
                "error": f"Invalid model response: '{response}'. Expected one of: {available_directions}"
            }

        # Execute the move
        try:
            self.maze.move(move)
            self.steps_taken += 1
            self.moves_history.append(move)

            # Check if maze is solved
            current_position = self.maze.position()
            is_solved = self.maze.solved()

            if is_solved:
                print(f"🎉 Maze solved in {self.steps_taken} steps!")
                self.is_solved = True

            # Display the updated maze
            self.maze.print()

            return {
                "success": True,
                "move": move,
                "position": current_position,
                "solved": is_solved,
                "steps_taken": self.steps_taken
            }

        except ValueError as e:
            return {
                "success": False,
                "move": move,
                "position": self.maze.position(),
                "solved": False,
                "error": f"Error executing move: {str(e)}"
            }

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the maze solving progress.
        
        Returns:
            Dict with solving statistics
        """
        return {
            "steps_taken": self.steps_taken,
            "moves_history": self.moves_history,
            "is_solved": self.is_solved,
            "start_position": self.maze.start,
            "end_position": self.maze.end,
            "current_position": self.maze.position(),
            "maze_dimensions": (self.maze.width, self.maze.height)
        }

    def solved(self) -> bool:
        """
        Check if the maze is solved.
        
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self.is_solved
