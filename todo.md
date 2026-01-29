# TODOS

- prompt:
  - have the colored prompt, through config, provide the number of numbered cells or not (from a given bool)
- live chat system:
  - to have quick feedback loop, implement chat like functionality.
  - add a way to go back one step in the prompt history in this tool.

## minor:

- prompt:
  - have steps_summary provide last n steps, passing n as an argument (to be finished)
- check and understand history max length
- check the context length:
  understand context length limits
- add full messages history passed per exchange in the chat_history object and visualizer
- maze filter:
  if 100 attempts at start and target generation fail, change the structure of the maze itself as it could simply be a lattice maze with no elegible start and target for the given filter
- stats:
  - Programmatically create summary tables

## Thoughts

### history length importance

The history seems to help quite a bit, although still no real reasoning is detected

The execution time does not really vary a lot when smaller prompt (i.e. without history) are passed, so I believe that history dimension does not really affect execution times.
Still it could be that the no history version takes a lot more steps than the history aided experiment, so the times even out for that reason.
This seems to be confirmed by the mean step execution times (15s for the first experiment, 12s for the no history experiment)

## default temperature

The default temperature for a <model> can be checked using this command:

```sh
ollama show --parameters <model> | grep temperature
```

If nothing is printed, then the default value of 0.8 is used [source](https://github.com/ollama/ollama/issues/6410)
