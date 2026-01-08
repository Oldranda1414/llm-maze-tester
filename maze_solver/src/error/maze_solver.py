from abc import abstractmethod, ABC


class MazeSolverError(Exception, ABC):
    """Base exception for all AutoDev errors."""

    def __init__(self):
        super().__init__(self.build_message())

    @abstractmethod
    def build_message(self) -> str:
        """Build the error message. Must be implemented by subclasses."""
        pass
