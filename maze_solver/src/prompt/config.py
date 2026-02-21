from dataclasses import dataclass


@dataclass(frozen=True)
class PromptConfig:
    provide_legal_output_hint: bool
    provide_spacial_awerness_hint: bool
    provide_color_hint: bool
    provide_repetition_hint: bool
    provide_avoid_dead_end: bool
    provide_steps_summary: int | None
    provide_possible_moves: bool
    provide_cot_reminder: bool
