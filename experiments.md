# Experiments

The folliwing details the approaches taken for the Experiments

## 2025-11-12_16:55:10

reference commit:
5992960026932015ca81ffa6fa3ca4c0e6e8056a

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

reference commit:
5992960026932015ca81ffa6fa3ca4c0e6e8056a

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

## no history, remove trivial mazes (2025-12-03_15:29:13)

commit reference:
91bf078afd5b26362a9686b1b6d60690eff70736

Given the results in experiment 11-14 it seems that some mazes have trivial solutions and they dirty the results.

A filter has been added to the maze generation to ensure that the generated mazes are not trivial
This experiment attempts to see if the filter works properly.

Once again no prompt history is provided so the expected hit rate is low (preferably 0%)

The filter seems to not have effect.

### Example

A notable example is the following prompt and reponse.

As is evident the exit is clearly stated to be in the south but it seems that the model still chooses to move in another direction, being utterly dumb.

- Prompt:

You are inside a maze. You have a compass with you. The maze is well lit so you can see in all directions how long the corridors are.
Just like a classic maze the exit is on the border. You could be anywhere in the maze as your starting position.
Your goal is to find the maze exit. Once you reach it you must step out of the maze with one last move.

Tell me which direction you would like to go to. Provide your answer in the form of the initial of the cardinal direction you wish to take a step forwards to.
The possible directions are N for north, E for east, S for south, W for west.


You are advised to think out loud about what your next move should be, but remember that the last thing you write must be a valid direction.

As an example if you want to step towards north the last character in your answer would be: N

You get as many turns as you want, so it's normal that at the start you have not enough information to know on what cell the exit is, so consider exploring to gather information at the start.

The maze is a 5 x 5 grid, with every square in the grid being one square meter big.
Due North there is a wall. You can't step in that direction.
Due East there is a corridor that goes on for one meter before encountering a wall. Although the corridor ends with a wall, you notice that some of the lateral paths along the way are open so it isn't a dead end.
Due South you can see the exit in that direction! One last step and you are out of the maze!
Due West there is a corridor that goes on for three meters before encountering a wall. Although the corridor ends with a wall, you notice that some of the lateral paths along the way are open so it isn't a dead end.

The moves you have made till now are: North, South, South, West, East, North, South, North, South, West, West, West, West, East, West, North, South, East, West, East, West, East, East, East, West, East
Your possible moves are: E, W, S.
After thinking it through, provide your next move.

- Response:

Let's think this through... I've been exploring and gathering information. I know the exit is due South, but I also don't want to get stuck in a dead-end situation. Since my last few moves have been mostly West and East, I think it's time to head back towards the middle of the maze.

I'm going to take a step back and reassess my options... Hmmm... Given that I know the exit is due South and there are walls in the North and East directions, I think my best bet is to move West. This will give me more information about what's ahead and potentially lead me closer to the exit.

So, my next move is: W

## Summary table

| Date  | Hit Rate (3×3) | Hit Rate (4×4) | Hit Rate (5×5) | Hit Rate (6×6) | Overall Hit Rate |
|-------|-----------------|-----------------|-----------------|-----------------|-------------------|
| 11-12 | 100.00%         | 100.00%         | 60.00%          | 40.00%          | 75.00%            |
| 11-14 | 80.00%          | 60.00%          | 60.00%          | 30.00%          | 57.50%            |

| Date  | Exec Time (3×3) | Exec Time (4×4) | Exec Time (5×5) | Exec Time (6×6) | Total Exec Time |
|-------|------------------|------------------|------------------|------------------|------------------|
| 11-12 | 00:54:37         | 01:58:10         | 05:37:37         | 10:15:30         | 18:45:54         |
| 11-14 | 01:37:08         | 03:15:02         | 05:00:59         | 10:28:34         | 20:21:43         |

