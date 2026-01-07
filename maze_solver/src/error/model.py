from error.maze_solver import MazeSolverError

class ModelNameError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model

    def build_message(self) -> tuple[str, ...]:
        return (
            f"Model name '{self.model}' is not a valid model name.",
            "To see all valid model names run 'just run --list'."
        )

class ModelAlreadyInstalledError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model

    def build_message(self) -> tuple[str, ...]:
        return (
            f"Model {self.model} is already installed.",
            "To see all installed models run 'just run --list'."
        )

class ModelNotInstalledError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model

    def build_message(self) -> tuple[str, ...]:
        return (
            f"Model {self.model} is not installed.",
            "To see all installed models run 'just run --list'."
        )

class ModelNotInitializedError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model

    def build_message(self) -> tuple[str, ...]:
        return (
            f"Model {self.model} is not initialized.",
            "To initialize the model call model.set_system_prompt()"
        )
