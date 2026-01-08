import yaml

from chat_history import ChatHistory
from maze import Maze
from maze.factory import maze_from_yaml
from maze.core.coordinate import Coordinate
from util import set_path


class Run:
    def __init__(
        self,
        maze: Maze,
        chat_history: ChatHistory,
        illegal_directions: int,
        illegal_responses: int,
        execution_time: float,
    ):
        self._maze = maze
        self._chat_history = chat_history
        set_path(self._maze, chat_history.chat)
        self._illegal_directions = illegal_directions
        self._illegal_responses = illegal_responses
        self._execution_time = execution_time

    @property
    def maze(self) -> Maze:
        return self._maze

    @property
    def chat_history(self) -> ChatHistory:
        return self._chat_history

    @property
    def illegal_directions(self) -> int:
        return self._illegal_directions

    @property
    def illegal_responses(self) -> int:
        return self._illegal_responses

    @property
    def execution_time(self) -> float:
        return self._execution_time

    @property
    def is_solved(self) -> bool:
        return self._maze.solved

    @property
    def start_position(self) -> Coordinate:
        return self._maze.start

    @property
    def target_position(self) -> Coordinate:
        return self._maze.target

    @property
    def current_position(self) -> Coordinate:
        return self._maze.position

    @property
    def maze_size(self) -> int:
        return self._maze.size

    @property
    def unique_positions_visited(self) -> int:
        return len(set(self._maze.path))

    def save(self, path: str):
        """Save the run to a YAML file."""
        data = {
            "maze": yaml.safe_load(self._maze.to_yaml()),
            "chat_history": yaml.safe_load(self._chat_history.to_yaml()),
            "illegal_directions": self._illegal_directions,
            "illegal_responses": self._illegal_responses,
            "execution_time": self._execution_time,
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
