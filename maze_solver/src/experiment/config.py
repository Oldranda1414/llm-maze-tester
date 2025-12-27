from dataclasses import dataclass
from pathlib import Path
import yaml

from model import Model
from model.factory import llm_model

@dataclass(frozen=True)
class ExperimentConfig:
    models: list[Model]
    maze_sizes: list[int]
    iterations: int
    provide_history: bool

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ExperimentConfig":
        path = Path(path)
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise SystemExit(f"Error: config file not found: {path}")
        except yaml.YAMLError as e:
            raise SystemExit(f"Error: invalid YAML in {path}: {e}")

        # ---- validate presence and types ----
        required = {
            "model_names": list,
            "maze_sizes": list,
            "iterations": int,
            "provide_history": bool,
        }

        for key, typ in required.items():
            if key not in data:
                raise SystemExit(f"Error: missing required field '{key}'")
            if not isinstance(data[key], typ):
                raise SystemExit(f"Error: '{key}' must be of type {typ.__name__}")

        # ---- validate elements of lists ----
        if not all(isinstance(x, str) for x in data["model_names"]):
            raise SystemExit("Error: 'model_names' must contain only strings")
        if not all(isinstance(x, int) for x in data["maze_sizes"]):
            raise SystemExit("Error: 'maze_sizes' must contain only integers")

        # ---- semantic checks ----
        if not data["model_names"]:
            raise SystemExit("Error: 'model_names' cannot be empty")
        if not data["maze_sizes"]:
            raise SystemExit("Error: 'maze_sizes' cannot be empty")
        if data["iterations"] <= 0:
            raise SystemExit("Error: 'iterations' must be > 0")

        model_names = data.pop("model_names", [])
        data["models"] = [llm_model(name) for name in model_names]

        return cls(**data)
