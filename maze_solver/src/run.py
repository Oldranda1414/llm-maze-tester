import yaml

from chat_history import ChatHistory
from maze import Maze
from maze.factory import maze_from_yaml
from move import Coordinate

class Run:
    def __init__(self, maze: Maze, chat_history: ChatHistory, illegal_directions: int, illegal_responses: int, execution_time: float):
        self.maze = maze
        self.chat_history = chat_history
        self._illegal_directions = illegal_directions
        self._illegal_responses = illegal_responses
        self._execution_time = execution_time

    def illegal_directions(self) -> int:
        return self._illegal_directions

    def illegal_responses(self) -> int:
        return self._illegal_responses

    def execution_time(self) -> float:
        return self._execution_time

    def is_solved(self) -> bool:
        return self.maze.solved()

    def start_position(self) -> Coordinate:
        return self.maze.start()

    def target_position(self) -> Coordinate:
        return self.maze.target()

    def current_position(self) -> Coordinate:
        return self.maze.position()

    def maze_dimension(self) -> int:
        return self.maze.size()

    def unique_positions_visited(self) -> int:
        return len(set(self.maze.path()))

    def save(self, path: str):
        """Save the run to a YAML file."""
        data = {
            "maze": yaml.safe_load(self.maze.to_yaml()),
            "chat_history": yaml.safe_load(self.chat_history.to_yaml()),
            "illegal_directions": self._illegal_directions,
            "illegal_responses": self._illegal_responses,
            "execution_time": self._execution_time
        }
        with open(path, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)

    @classmethod
    def load(cls, path: str) -> "Run":
        """Load a run (maze + chat history) from a YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        maze_data = yaml.safe_dump(data["maze"])
        chat_data = yaml.safe_dump(data["chat_history"])
        i_d = data["illegal_directions"] 
        i_r = data["illegal_responses"]
        execution_time = data["execution_time"]

        maze = maze_from_yaml(maze_data)
        chat_history = ChatHistory.from_yaml(chat_data)

        return cls(maze, chat_history, i_d, i_r, execution_time)
