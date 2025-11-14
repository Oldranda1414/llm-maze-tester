# TODOS

- prompt
    - history max length
- check the context lenght:
    ```
    prompt_tokens = response.get("prompt_eval_count")
    print(f"Prompt tokens used: {prompt_tokens}")
    ```
- add full messages history passed per exchange in the chat_history object and visualizer

## bugs:

- maze
    - when seed is 39
        - solve warning reset global seed
        - solve maze exit output wrong, only cli

### New concept
Have a short version of the prompt generation (step_prompt() != step_prompt_short()).
Use it to condense the history except the last prompt.
Also consider removing erroneus prompts.

