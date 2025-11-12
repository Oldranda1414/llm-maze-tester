# TODOS

- move
    - refactor Coordinate to Cell
- prompt
    - history max length
- run
    - for [3,4,5,6,7] run 10 simulations with different maze and analyse hit rate
- maze
    - when seed is 39
        - solve warning reset global seed
        - solve maze exit output wrong, only cli
    - have path consider the last move also. As of now no maze loaded can be solved.

history condensata, controllare input massimo

### New concept
Have a short version of the prompt generation (step_prompt() != step_prompt_short()).
Use it to condense the history except the last prompt.
Also consider removing erroneus prompts.
