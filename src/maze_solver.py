"""
maze_solver.py
A class that uses an LLM model to solve a maze.
"""
from typing import Dict, Any, List, Set, Tuple

from model import Model
from maze import Direction, Maze
from prompt import generate_step_prompt, get_preamble

class MazeSolver:
    """
    A class that uses an LLM model to solve a maze.
    The solver initializes a model and a maze, then prompts the model
    to make decisions about which direction to move at each step.
    """

    def __init__(self, model_name: str, maze_width: int = 6, maze_height: int = 6,
                 plot: bool = False):
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
                        plot=plot)

        # Statistics and tracking
        self.steps_taken = 0
        self.moves_history: List[str] = []
        self.visited_positions: Set[Tuple[int, int]] = set()
        self.is_solved = False
        self.position_history: List[Tuple[int, int]] = []
        self.plot = plot

        # Show the initial maze state
        self.maze.print()

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

        prompt = ""

        if self.steps_taken == 0:
            prompt += get_preamble(self.maze)

        prompt += generate_step_prompt(self.maze)

        response = self.model.ask(prompt)
        print(f"Model response: {response}")
        print(f"available_directions: {available_directions}")

        move = None
        # TODO remove for, should only check if the provided move is a char, otherwise notify that the response is not valid
        for char in response:
            print(f"char in reponse: {char}")
            if char.upper() in ["N", "S", "W", "E"] and char.upper() in [direction.to_coordinate() for direction in available_directions]:
                print("setting move")
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
            print(move)
            print(Direction.from_coordinate(move))
            valid_move = self.maze.move(Direction.from_coordinate(move))
            print(f"move accepted: {valid_move}")
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
