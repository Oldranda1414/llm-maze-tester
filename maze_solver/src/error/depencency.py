from error.maze_solver import MazeSolverError

class OllamaNotInstalledError(MazeSolverError):
    exit_code = 11

    def __init__(self):
        super().__init__()
        super().__init__()

    def build_message(self) -> str:
        return (
            "Ollama does not seem to be installed on the system.\n"
            "Run 'nix develop' to enter development shell and install ollama temporarily or visit https://ollama.com/ to checkout how to install ollama permanently on your system."
        )

