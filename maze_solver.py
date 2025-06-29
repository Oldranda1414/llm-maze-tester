"""
maze_solver.py
A class that uses an LLM model to solve a maze.
"""
from typing import Dict, Any, List, Set, Tuple

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
        {pattern_warning}
        
        Your move history: {move_history}

        Choose your next move (respond with only a single letter: {move_options}):
    """

    # Template for pattern warning
    PATTERN_WARNING = """
        WARNING: You appear to be stuck in a repetitive pattern: {pattern}
        Try to choose a different strategy to reach the goal.
    """

    def __init__(self, model_name: str, maze_width: int = 6, maze_height: int = 6,
                 plot: bool = True, block_on_plot: bool = False, pattern_check_length: int = 6):
        """
        Initialize the maze solver with a model and maze.
        
        Args:
            model_name: Name of the LLM model to use
            maze_width: Width of the maze
            maze_height: Height of the maze
            plot: Whether to display the maze graphically
            block_on_plot: Whether to block execution when showing plots
            pattern_check_length: Number of recent moves to check for patterns
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
        self.visited_positions: Set[Tuple[int, int]] = set()
        self.is_solved = False
        self.pattern_check_length = pattern_check_length
        self.position_history: List[Tuple[int, int]] = []
        self.plot = plot

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

    # def _detect_pattern(self) -> tuple[bool, str]:
    #     """
    #     Detect repetitive patterns in recent moves.
        
    #     Returns:
    #         tuple: (pattern_detected, pattern_description)
    #     """
    #     warning_message = "You are moving in a repetitive pattern. Please try to change your strategy. Use the move history to better orient yourself."

    #     if len(self.moves_history) < 4:
    #         return False, ""

    #     # Check for simple alternating patterns (e.g., "UDUD" or "LRLR")
    #     recent_moves = ''.join(self.moves_history[-self.pattern_check_length:])

    #     # Check for 2-move pattern (e.g., "UDUD")
    #     for pattern_len in [2, 3, 4]:
    #         if len(recent_moves) >= pattern_len * 2:
    #             pattern = recent_moves[-pattern_len:]
    #             prev_pattern = recent_moves[-(2*pattern_len):-pattern_len]

    #             if pattern == prev_pattern:
    #                 return True, f"'{pattern}' repeating"

    #     # Check for oscillating between two positions
    #     if len(self.position_history) >= 4:
    #         recent_positions = self.position_history[-4:]
    #         if recent_positions[0] == recent_positions[2] and recent_positions[1] == recent_positions[3]:
    #             return True, warning_message

    #     return False, ""

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
        if self.is_solved:
            return {
                "success": False,
                "move": None,
                "position": self.maze.position(),
                "solved": True,
                "error": "Maze already solved"
            }

        available_directions = self.maze.get_directions()
        # pattern_detected, pattern_desc = self._detect_pattern()
        pattern_warning = ""
        # if pattern_detected:
        #     pattern_warning = self.PATTERN_WARNING.format(pattern=pattern_desc)
        #     print(f"Warning: Detected pattern - {pattern_desc}")

        move_history = ", ".join(self.moves_history) if self.moves_history else "None (first move)"
        prompt = self.STEP_PROMPT.format(
            current_pos=self.maze.position(),
            end_pos=self.maze.end,
            available_moves=", ".join(available_directions),
            move_options=", ".join(available_directions),
            pattern_warning=pattern_warning,
            move_history=move_history
        )

        response = self.model.ask(prompt)
        print(f"Model response: {response}")

        move = None
        for char in response:
            if char.upper() in ["U", "D", "L", "R"] and char.upper() in available_directions:
                move = char.upper()
                break

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
            valid_move = self.maze.move(move)
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
                self.maze.print()

                return {
                    "success": True,
                    "move": move,
                    "position": new_position,
                    "solved": is_solved,
                    "steps_taken": self.steps_taken,
                    # "pattern_detected": pattern_detected
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
            "maze_dimensions": (self.maze.width, self.maze.height),
            "unique_positions_visited": len(self.visited_positions)
        }

    def solved(self) -> bool:
        """
        Check if the maze is solved.
        
        Returns:
            bool: True if the maze is solved, False otherwise
        """
        return self.is_solved
