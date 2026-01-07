from error.maze_solver import MazeSolverError

class ModelRequestError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model

    def build_message(self) -> tuple[str, ...]:
        return (
            f"Model {self.model} was unable to generate a response, due to a request error.",
        )

