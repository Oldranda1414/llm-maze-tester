from abc import abstractmethod

class MazeSolverError(Exception):
    """Base exception for all AutoDev errors."""

    def __init__(self):
        super().__init__(self.build_message())

    @abstractmethod
    def build_message(self) -> tuple[str, ...]:
        """Build the error message. Must be implemented by subclasses."""
        pass

