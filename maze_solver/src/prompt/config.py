from dataclasses import dataclass


@dataclass(frozen=True)
class PromptConfig:
    provide_steps_summary: int | None
    provide_possible_moves: bool
