# TODOS

- prompt
    - have steps_summary provide last n steps, passing n as an argument
- stats:
    - Programmatically create summary tables

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
