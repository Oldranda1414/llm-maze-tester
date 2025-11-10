import yaml
from chat_history import ChatHistory
from maze import Maze
from maze.factory import maze_from_yaml

class Run:
    def __init__(self, maze: Maze, chat_history: ChatHistory):
        # path_length = len(maze.path())
        # if not maze.solved():
        #     path_length += 1
        # if path_length != len(chat_history.chat):
        #     raise ValueError(f"Chat history ({len(chat_history.chat)}) and maze path ({path_length}) lenghts are not compatibile")

        self.maze = maze
        self.chat_history = chat_history

    def save(self, path: str):
        """Save the run (maze + chat history) to a YAML file."""
        data = {
            "maze": yaml.safe_load(self.maze.to_yaml()),
            "chat_history": yaml.safe_load(self.chat_history.to_yaml()),
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

        maze = maze_from_yaml(maze_data)
        chat_history = ChatHistory.from_yaml(chat_data)

        return cls(maze, chat_history)

