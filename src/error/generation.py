from error.maze_solver import MazeSolverError

class ModelTimeoutError(MazeSolverError):
    def __init__(self, model: str, request_timeout: int):
        self.model = model
        self.request_timeout = request_timeout

    def build_message(self) -> tuple[str, ...]:
        return (
            f"Model {self.model} was unable to generate a response in {self.request_timeout} seconds.",
        )

