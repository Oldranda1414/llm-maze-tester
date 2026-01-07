from error.maze_solver import MazeSolverError

class ModelRequestError(MazeSolverError):
    def __init__(self, model: str):
        self.model = model
        super().__init__()

    def build_message(self) -> str:
        return f"Model {self.model} was unable to generate a response, due to a request error."

