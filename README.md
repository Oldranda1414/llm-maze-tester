# llm-maze-tester

## Introduction

This project aims to test the ability of various foundational models to navigate and solve a maze

To run the project:

`uv run main.py`

## Tech

### UV

This project uses uv python package manager

Python dependencies are listed in the `pyproject.toml` file.

### Ollama

This project uses [Ollama](https://ollama.com/) to run the models locally.

### maze-dataset

[maze-dataset](https://github.com/understanding-search/maze-dataset) library is used to generate and print the maze

### Design

Class Diagram

```mermaid
classDiagram
    class Model {
        +String model_name
        +List~Dict~ chat_history
        +String base_url
        +String base_model
        +__init__(model_name: str)
        +ask(prompt: str) str
        +history() List~Dict~
        +save(filepath: str) bool
        +reset_chat() void
    }
    
    class Maze {
        +int width
        +int height
        +bool plot
        +bool block_on_plot
        +TargetedLatticeMaze maze
        +Tuple start
        +Tuple end
        +__init__(width, height, plot, block_on_plot)
        +move(direction) bool
        +get_directions()
        +position()
        +solved()
        +print()
    }
    
    class MazeSolver {
        +Model model
        +Maze maze
        +int steps_taken
        +List~str~ moves_history
        +bool is_solved
        +String INITIAL_PROMPT
        +String STEP_PROMPT
        +__init__(model_name: str, maze_width: int, maze_height: int, plot: bool, block_on_plot: bool)
        -_send_initial_prompt()
        +step() Dict~str, Any~
        +get_statistics() Dict~str, Any~
        +solved() bool
    }
    
    class litellm {
        <<library>>
    }
    
    class requests {
        <<library>>
    }
    
    class maze_dataset {
        <<library>>
    }
    
    class matplotlib {
        <<library>>
    }
    
    class numpy {
        <<library>>
    }
    
    Model --> litellm : uses for completions
    Model --> requests : API calls
    Maze --> maze_dataset : generation
    Maze --> matplotlib : visualization
    Maze --> numpy : data handling
    MazeSolver --> Model : has
    MazeSolver --> Maze : has
```
