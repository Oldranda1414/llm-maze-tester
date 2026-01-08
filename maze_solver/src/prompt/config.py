from dataclasses import dataclass


@dataclass(frozen=True)
class PromptConfig:
    provide_steps_summary: bool
    provide_possible_moves: bool
