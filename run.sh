#!/usr/bin/env sh

mkdir -p results/logs
uv --project maze_solver run maze_solver/src/main.py > "results/logs/$(date +%Y-%m-%d).log"

