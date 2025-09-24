set quiet

# List available recipies
default:
  just --list --unsorted --list-heading $'Available commands:\n'

# Run the project
[no-exit-message]
run *args:
  just withOllama uv --project src run src/main.py {{args}}

# Run the prompt generation test
[no-exit-message]
prompt *args:
  just withOllama uv --project src run src/prompt_test.py {{args}}

[no-exit-message]
withOllama *args:
  ./withOllama.sh {{args}}

# Add package to project dependencies
[no-exit-message]
add *args:
  uv --project src add {{args}}

