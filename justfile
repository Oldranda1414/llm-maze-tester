set quiet

# List available recipies
default:
  just --list --unsorted --list-heading $'Available commands:\n'

# Run the project
[no-exit-message]
run *args:
  uv --project src run src/main.py {{args}}

# Run the prompt generation test
[no-exit-message]
prompt *args:
  uv --project src run src/prompt_test.py {{args}}

# Run the maze-prompt example
[no-exit-message]
example *args:
  uv --project src run src/prompt_example.py {{args}}

# Run the maze test
[no-exit-message]
maze *args:
  uv --project src run src/maze_test.py {{args}}

# Run the model test
[no-exit-message]
model *args:
  uv --project src run src/model_test.py {{args}}

# Add package to project dependencies
[no-exit-message]
add *args:
  uv --project src add {{args}}

# Add package to project dependencies
[no-exit-message]
remove *args:
  uv --project src remove {{args}}

