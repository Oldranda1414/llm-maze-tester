# TODOS

- prompt
    - history max length
    - add reminder on legal output format in every step prompt
- check the context lenght:
    ```
    prompt_tokens = response.get("prompt_eval_count")
    print(f"Prompt tokens used: {prompt_tokens}")
    ```
- add full messages history passed per exchange in the chat_history object and visualizer
- maze filter:
    if 100 attempts at start and target generation fail, change the structure of the maze itself as it could simply be a lattice maze with no elegible start and target for the given filter

## bugs:

- maze
    - when seed is 39
        - solve warning reset global seed
        - solve maze exit output wrong, only cli

### New concept

Have a short version of the prompt generation (step_prompt() != step_prompt_short()).
Use it to condense the history except the last prompt.
Also consider removing erroneus prompts.

### Ideas

Have the output from the llm solver be passed as input to another llm with the only goal of determining given the input provide the sanitised output, i.e. the direction the solver wants to move to.

### Thoughts

The history seems to help quite a bit, although still no real reasoning is detected

The execution time does not really vary a lot when smaller prompt (i.e. without history) are passed, so I believe that history dimension does not really affect execution times.
Still it could be that the no history version takes a lot more steps than the history aided experiment, so the times even out for that reason.
This seems to be confirmed by the mean step execution times (15s for the first experiment, 12s for the no history experiment)

