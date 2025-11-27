# Experiments

The folliwing details the approaches taken for the Experiments

## 2025-11-12_16:55:10

The goal is to test if illigal_direction numbers lower when providing the available directions explicitly

Full history passed.

The following format is used:

'''
The moves you have made till now are: W, E, W, E, W, E, S
Your possible moves are: N, S, E.
After thinking it through, provide your next move.
'''

### Stats

=== Maze size: 3 ===
mean_illegal_directions: 0.40
perc_illegal_directions: 0.88
mean_illegal_responses: 2.90
perc_illegal_responses: 11.51
mean_total_steps: 22.70
mean_decisions: 19.80
perc_solved: 100.00
mean_execution_time: 00:05:28
total_execution_time: 00:54:37

=== Maze size: 4 ===
mean_illegal_directions: 2.20
perc_illegal_directions: 3.03
mean_illegal_responses: 16.50
perc_illegal_responses: 24.33
mean_total_steps: 46.40
mean_decisions: 29.90
perc_solved: 100.00
mean_execution_time: 00:11:49
total_execution_time: 01:58:10

=== Maze size: 5 ===
mean_illegal_directions: 5
perc_illegal_directions: 4.39
mean_illegal_responses: 39
perc_illegal_responses: 26.41
mean_total_steps: 130.80
mean_decisions: 91.80
perc_solved: 60.00
mean_execution_time: 00:33:46
total_execution_time: 05:37:37

=== Maze size: 6 ===
mean_illegal_directions: 4.50
perc_illegal_directions: 3.56
mean_illegal_responses: 62.60
perc_illegal_responses: 20.07
mean_total_steps: 238.10
mean_decisions: 175.50
perc_solved: 40.00
mean_execution_time: 01:01:33
total_execution_time: 10:15:30

=== Overall stats ===
mean_illegal_directions: 3.02
perc_illegal_directions: 2.96
mean_illegal_responses: 30.25
perc_illegal_responses: 20.58
mean_total_steps: 109.50
mean_decisions: 79.25
perc_solved: 75.00
mean_execution_time: 00:28:09
total_execution_time: 18:45:54

## 2025-11-14_13:19:12

The goal is to test if the history actually helps the llm.

So the history is never passed to the model.

The model receives the system prompt, the preamble and the step info every step.

### Stats

=== Maze size: 3 ===
mean_illegal_directions: 1.10
perc_illegal_directions: 2.66
mean_illegal_responses: 16.40
perc_illegal_responses: 32.95
mean_total_steps: 48.40
mean_decisions: 32
perc_solved: 80.00
mean_execution_time: 00:09:43
total_execution_time: 01:37:08

=== Maze size: 4 ===
mean_illegal_directions: 2.40
perc_illegal_directions: 3.93
mean_illegal_responses: 33.80
perc_illegal_responses: 33.85
mean_total_steps: 96.30
mean_decisions: 62.50
perc_solved: 60.00
mean_execution_time: 00:19:30
total_execution_time: 03:15:02

=== Maze size: 5 ===
mean_illegal_directions: 2.20
perc_illegal_directions: 1.71
mean_illegal_responses: 60.10
perc_illegal_responses: 39.55
mean_total_steps: 147.70
mean_decisions: 87.60
perc_solved: 60.00
mean_execution_time: 00:30:06
total_execution_time: 05:00:59

=== Maze size: 6 ===
mean_illegal_directions: 3.70
perc_illegal_directions: 1.04
mean_illegal_responses: 121.30
perc_illegal_responses: 38.74
mean_total_steps: 307.30
mean_decisions: 186
perc_solved: 30.00
mean_execution_time: 01:02:51
total_execution_time: 10:28:34

=== Overall stats ===
mean_illegal_directions: 2.35
perc_illegal_directions: 2.33
mean_illegal_responses: 57.90
perc_illegal_responses: 36.27
mean_total_steps: 149.93
mean_decisions: 92.03
perc_solved: 57.50
mean_execution_time: 00:30:33
total_execution_time: 20:21:43

## Summary table


| Date  | Perc_solved (3) | Perc_solved (4) | Perc_solved (5) | Perc_solved (6) | Perc_solved (Total) | Exec time (3) | Exec time (4) | Exec time (5) | Exec time (6) | Total Exec Time |
|-------|------------------|------------------|------------------|------------------|-----------------------|----------------|----------------|----------------|----------------|------------------|
| 11-12 | 100.00           | 100.00           | 60.00            | 40.00            | 75.00                | 00:54:37       | 01:58:10       | 05:37:37       | 10:15:30       | 18:45:54         |
| 11-14 | 80.00            | 60.00            | 60.00            | 30.00            | 57.50                | 01:37:08       | 03:15:02       | 05:00:59       | 10:28:34       | 20:21:43         |
