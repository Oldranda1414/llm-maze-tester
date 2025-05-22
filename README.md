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

This project uses Ollama to run the models locally. You can find more information about it [here](https://ollama.com/).

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
        +\_\_init__(model_name: str)
        +ask(prompt: str) str
        +history() List~Dict~
        +save(filepath: str) bool
    }
    
    class Maze {
        +int width
        +int height
        +bool plot
        +bool block_on_plot
        +TargetedLatticeMaze maze
        +Tuple start
        +Tuple end
        +\_\_init__(width, height, plot, block_on_plot)
        +move(direction)
        +get_directions()
        +position()
        +solved()
        +print()
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
```
