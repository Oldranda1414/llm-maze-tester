# TODOS

- prompt
    - have steps_summary provide last n steps, passing n as an argument
- stats:
    - Programmatically create summary tables
- to-mp3:
    - implement a way to turn the maze resolving into an mp3 video, with maze, path, prompt ecc.
- experiments:
    - have experiments save themselves with commit hashes so that it is easy to check the conditions the experiment was executed in.

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

