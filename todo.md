# TODOS

- prompt
    - have steps_summary provide last n steps, passing n as an argument
- stats:
    - Programmatically create summary tables

## bugs:
- stats:
    - mean decisions seems to not be computed correctly:
        - 'just stats 2026-01-08_16:23:34' displays 'mean decisions: 0.00'

## minor:

- check and understand history max length
- check the context length:
    understand context length limits
- add full messages history passed per exchange in the chat_history object and visualizer
- maze filter:
    if 100 attempts at start and target generation fail, change the structure of the maze itself as it could simply be a lattice maze with no elegible start and target for the given filter


## New concept

Have a short version of the prompt generation (step_prompt() != step_prompt_short()).
Use it to condense the history except the last prompt.
Also consider removing erroneus prompts.

## Ideas

Have the output from the llm solver be passed as input to another llm with the only goal of determining given the input provide the sanitised output, i.e. the direction the solver wants to move to.

### Thoughts

#### history length importance

The history seems to help quite a bit, although still no real reasoning is detected

The execution time does not really vary a lot when smaller prompt (i.e. without history) are passed, so I believe that history dimension does not really affect execution times.
Still it could be that the no history version takes a lot more steps than the history aided experiment, so the times even out for that reason.
This seems to be confirmed by the mean step execution times (15s for the first experiment, 12s for the no history experiment)

#### prompt truncation

Now the program throws an exception when prompt length is over the limit, although this is known only after the model returns it's response.
Also it seems that the end of the prompt is truncated, and not the start of the prompt as expected.
Further tests with prompt history will be done.

### Working ds prompt

The following preamble worked with deepseek-r1

You are inside a maze. You have a compass with you. The maze is well lit so you can see in all directions how long the corridors are.
Just like a classic maze the exit is on the border. You could be anywhere in the maze as your starting position.
Your goal is to find the maze exit. Once you reach it you must step out of the maze with one last move.

Tell me which direction you would like to go to. Provide your answer in the form of the initial of the cardinal direction you wish to take a step forwards to.
The possible directions are N for north, E for east, S for south, W for west.

As an example if you want to step towards north the last character in your answer would be: N

You get as many turns as you want, so it's normal that at the start you don't have enough information to know on what cell the exit is, so consider exploring to gather information at the start.

The maze is a 3 x 3 grid, with every square in the grid being one square meter big.

Due North there is a wall. You can't step in that direction.
Due East there is a wall. You can't step in that direction.
Due South there is a corridor that goes on for two meters before encountering a wall. Although the corridor ends with a wall, you notice that some of the lateral paths along the way are open so it isn't a dead end.
Due West there is a wall. You can't step in that direction.
Your possible moves are: S.
What is your next move?

