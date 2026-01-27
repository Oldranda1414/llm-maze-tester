set quiet

# List available recipies
default:
  just --list --unsorted --list-heading $'Available commands:\n'

# MAINS

# Run the project
[no-exit-message]
run *args:
  uv --project maze_solver run maze_solver/src/main.py {{args}}

# Print stats for a given experiment
[no-exit-message]
stats *args:
  uv --project maze_solver run maze_solver/src/stats_main.py {{args}}

# Render a run
[no-exit-message]
render *args:
  uv --project maze_solver run maze_solver/src/render_main.py {{args}}

# Run the cli chat
[no-exit-message]
chat *args:
  uv --project maze_solver run maze_solver/src/chat_main.py {{args}}

# Run a given test
[no-exit-message]
test *args:
  uv --project maze_solver run maze_solver/src/test_main.py {{args}}

# MISC

# Open visualizer
[no-exit-message]
visualize:
  uv --project maze_solver run python -m jupyterlab maze_solver/src/visualize.ipynb > /dev/null 2>&1 & \
  read -p "Press ENTER to stop Jupyter... " _; \
  git restore maze_solver/src/visualize.ipynb; \
  pkill -f jupyter-lab; 

# Copy results folder from server
[no-exit-message]
copy:
  rsync -avz -e ssh lrandacio@137.204.72.12:/home/lrandacio/llm-maze-tester/results .

# UV

# Add package to project dependencies
[no-exit-message]
add *args:
  uv --project maze_solver add {{args}}

# Add package to project dependencies
[no-exit-message]
remove *args:
  uv --project maze_solver remove {{args}}

