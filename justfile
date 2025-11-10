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

# Run the run test
[no-exit-message]
run_test *args:
  uv --project maze_solver run maze_solver/src/run_test.py {{args}}

# Run the visualizer test
[no-exit-message]
vis *args:
  uv --project maze_solver run maze_solver/src/visualizer_test.py {{args}}

# Add package to project dependencies
[no-exit-message]
add *args:
  uv --project maze_solver add {{args}}

# Add package to project dependencies
[no-exit-message]
remove *args:
  uv --project maze_solver remove {{args}}

# Open visualizer
[no-exit-message]
visualize:
  uv --project maze_solver run python -m jupyterlab maze_solver/src/visualizer_test.ipynb > /dev/null 2>&1 & \
  read -p "Press ENTER to stop Jupyter... " _; \
  git restore maze_solver/src/visualizer_test.ipynb; \
  pkill -f jupyter-lab; 

# Copy results folder from server
copy:
  rsync -avz -e ssh lrandacio@137.204.72.12:/home/lrandacio/llm-maze-tester/results ~/Downloads/
