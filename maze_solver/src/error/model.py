from error.maze_solver import MazeSolverError

class ModelNameError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model
        super().__init__()

    def build_message(self) -> str:
        return (
            f"Model name '{self.model}' is not a valid model name.\n"
            "To see all valid model names run 'just run --list'."
        )

class ModelAlreadyInstalledError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model
        super().__init__()

    def build_message(self) -> str:
        return (
            f"Model {self.model} is already installed.\n"
            "To see all installed models run 'just run --list'."
        )

class ModelNotInstalledError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model
        super().__init__()

    def build_message(self) -> str:
        return (
            f"Model {self.model} is not installed.\n"
            "To see all installed models run 'just run --list'."
        )

class ModelNotInitializedError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model
        super().__init__()

    def build_message(self) -> str:
        return (
            f"Model {self.model} is not initialized.\n"
            "To initialize the model call model.set_system_prompt()"
        )
