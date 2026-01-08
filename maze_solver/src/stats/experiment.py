from collections import defaultdict
import statistics

from experiment import Experiment
from util import seconds_to_padded_time


def print_experiment_stats(experiment: Experiment):
    """
    Computes and prints statistics on a list of Run objects.
    Statistics are grouped by maze size and also shown overall.
    """
    if not experiment.runs:
        print("No runs provided.")
        return

    # Organize runs by maze size
    runs_by_size = defaultdict(list)
    for run in experiment.runs:
        size = run.maze_size
        runs_by_size[size].append(run)

    # Print stats per maze size
    for size, run_list in sorted(runs_by_size.items()):
        stats = compute_stats(run_list)
        print(f"\n=== Maze size: {size} ===")
        for k, v in stats.items():
            if type(v) is float:
                v = f"{v:.2f}"
            print(f"{k}: {v}")

    # Compute overall stats
    overall_stats = compute_stats(experiment.runs)
    print("\n=== Overall stats ===")
    for k, v in overall_stats.items():
        if type(v) is float:
            v = f"{v:.2f}"
        print(f"{k}: {v}")


def compute_stats(run_list):
    total_steps_list = [len(r.chat_history.chat) for r in run_list]
    illegal_dirs_list = [r.illegal_directions for r in run_list]
    illegal_resps_list = [r.illegal_responses for r in run_list]
    decisions_list = [len(r.maze.decisions) for r in run_list]
    execution_list = [r.execution_time for r in run_list]
    solved_list = [r.is_solved for r in run_list]

    step_execution_times = [
        exec_t / steps
        for exec_t, steps in zip(execution_list, total_steps_list)
        if steps > 0
    ]
    mean_step_execution_seconds = statistics.mean(step_execution_times)
    mean_step_execution_time = seconds_to_padded_time(mean_step_execution_seconds)

    mean_illegal_dirs = statistics.mean(illegal_dirs_list)
    perc_illegal_dirs = statistics.mean(
        [
            id_ / ts * 100 if ts > 0 else 0
            for id_, ts in zip(illegal_dirs_list, total_steps_list)
        ]
    )

    mean_illegal_resps = statistics.mean(illegal_resps_list)
    perc_illegal_resps = statistics.mean(
        [
            ir / ts * 100 if ts > 0 else 0
            for ir, ts in zip(illegal_resps_list, total_steps_list)
        ]
    )

    mean_total_steps = statistics.mean(total_steps_list)
    mean_decisions = statistics.mean(decisions_list)
    perc_solved = sum(solved_list) / len(solved_list) * 100

    mean_execution = seconds_to_padded_time(statistics.mean(execution_list))
    total_execution = seconds_to_padded_time(sum(execution_list))

    return {
        "mean_illegal_directions": mean_illegal_dirs,
        "perc_illegal_directions": perc_illegal_dirs,
        "mean_illegal_responses": mean_illegal_resps,
        "perc_illegal_responses": perc_illegal_resps,
        "mean_total_steps": mean_total_steps,
        "mean_decisions": mean_decisions,
        "perc_solved": perc_solved,
        "mean_execution_time": mean_execution,
        "total_execution_time": total_execution,
        "mean_step_execution_time": mean_step_execution_time,
    }
