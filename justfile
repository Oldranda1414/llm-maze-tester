set quiet

# List available recipies
default:
  just --list --unsorted --list-heading $'Available commands:\n'

# Run the project
[no-exit-message]
run *args:
  ./run.sh

# Add package to project dependencies
[no-exit-message]
add *args:
  uv --project src add {{args}}

