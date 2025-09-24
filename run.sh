#!/usr/bin/env bash
set -euo pipefail

# Start ollama in the background
ollama serve >/dev/null 2>&1 &
pid=$!

# Ensure ollama is killed on exit or Ctrl-C
trap 'kill "$pid" 2>/dev/null || true' EXIT

# Run provided command
"$@"
