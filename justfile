set quiet

# List available recipies
default:
  just --list --unsorted --list-heading $'Available commands:\n'

# Run the project
[no-exit-message]
run *args:
  uv --project maze_solver run maze_solver/src/main.py {{args}}

# Run the prompt generation test
[no-exit-message]
prompt *args:
  uv --project maze_solver run maze_solver/src/prompt_test.py {{args}}

# Run the maze-prompt example
[no-exit-message]
example *args:
  uv --project maze_solver run maze_solver/src/prompt_example.py {{args}}

# Run the maze test
[no-exit-message]
maze *args:
  uv --project maze_solver run maze_solver/src/maze_test.py {{args}}

# Run the model test
[no-exit-message]
model *args:
  uv --project maze_solver run maze_solver/src/model_test.py {{args}}

# Run the model test
[no-exit-message]
run_test *args:
  uv --project maze_solver run maze_solver/src/run_test.py {{args}}

# Add package to project dependencies
[no-exit-message]
add_solver *args:
  uv --project maze_solver add {{args}}

# Add package to project dependencies
[no-exit-message]
remove_solver *args:
  uv --project maze_solver remove {{args}}

