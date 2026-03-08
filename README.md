# llm-maze-tester

## Introduction

This repo contains the source code for the master thesis 'Valutazione delle Capacità di Ragionamento dei Large Language Model: la risoluzione di labirinti' by Leonardo Randacio for the masters course 'Scienze e Ingegneria Informatiche' at 'Università di Bologna'.

This project aims to test the ability of various LLM models to navigate and solve a maze.

This project uses [Nix](https://nixos.org/download/) for dev env automation. To simplify dev tool installation, it is suggested to install [Nix](https://nixos.org/download/).

Once Nix in installed, to install the project dependencies and enter development shell run:

```sh
nix develop
```

Otherwise the following tools should be installed manually (refer to every tool's install documentation):

- [just](https://github.com/casey/just)
- [uv](https://docs.astral.sh/uv/)
- [ollama](https://ollama.com/)

### Disclaimer

This project has been developed on [Linux Mint](https://linuxmint.com/), using [LazyVim](https://www.lazyvim.org/).
Although it should be compatible with any other development environment, especially if the dependencies are installed through Nix, no tests have been done on other environments to validate this claim.

## Tech

### Nix

Nix is used for development environment automation

### Just

The project uses just to simplify cli commands

### UV

This project uses uv python package manager

Python dependencies are listed in the `pyproject.toml` file.

### Ollama

This project uses [Ollama](https://ollama.com/) to run the models locally.

### maze-dataset

[maze-dataset](https://github.com/understanding-search/maze-dataset) library is used to generate the lattice mazes using DFS algorithm.

### jupyter

jupyter notebooks are used for results visualization.

## Project Structure

The source code for the project is cont

### Python source

All the python source code is contained in `./maze_solver` directory.

`./maze_solver` contains:

- python source code:
  - `src`
- uv project and dependency definition files:
  - `uv.lock`
  - `pyproject.toml`
  - `.python-version`

The source (`src` directory) is organized as follows:

- `main.py`: entry point of the source, calls `*_main.py` files given the subcommand provided
- `*_main.py` files: entry points for all subcommands:
- `chat`: interactive chat functionalities
- `error`: primitive and undercooked custom error definitions
- `experiment`: experiment abstraction classes
- `generate`: images for the thesis generation
- `maze`: maze wrapper abstraction over maze-dataset library
- `model`: llm model abstraction over ollama python api
- `prompt`: prompt generation
- `render`: render run in mp4 file functionality
- `run`: run abstraction classes
- `stats`: experiment stats generation
- `test`: quick tests functionalities
- `visualize`: run visualization functionality

### run script

The `./run.sh` script is to easily run the experiment on systems (such as the uni server) where the just tool is not installed. The script needs only UV to be installed on the system to run the experiment given the configuration defined in `./maze_solver/src/experiemnt/config.py`

### experiments nots

The `experiments.md` file contains notes on the reasoning and results of the main experiments executed during the work on the thesis. It is rather discursive in nature, and meant more as my own personal use notes rather than a well documented log on the experiments.

### nix files

`flake.nix` and `flake.lock` files are [Nix](https://nixos.org/) files. The `flake.nix` file defines all the project tool dependencies, making the project's development environment fully reproducible.

### results folder

The `./results` directory contains all the run experiments.
The contents are structured as follows:

- `log`: directory containing all the cli output logs of all executions, organized by days. This is used only to check for exceptions during experiment execution. Usually experiments are run in silent mode so no actual output is expected.
- `yyyy-mm-dd_hh:mm:ss` directories: these directories are created with the timestamp of the experiment start and contain all the results.
  - `<model_name>` every experiment directory contains a directory for every model used in that experiment.
    - `<n>x<n>`: every model directory contains a directory for every labyrinth size tested (n = 1,...,7)
      - `<x>.yaml`: the actual experiment run log in yaml format. This file contains:
        - the git hash of the commit when the experiment was launched (to ensure stats compatibility)
        - the maze configuration used
        - the path taken by the model in during the experiment
        - the actual chat history from the experiment
        - some stats (such as the execution time)

### chat config folder

The `./chat` folder contains the files used for the interactive chat functionality (`just chat` command). These files are:

- `config.yaml`: where the model to be used is configured.
- `system_prompt.txt`: where the system_prompt for the chat exchange (used only once) is configured
- `prompt.txt`: where the prompt is read for every step. This file is meant to be changed every step with the new step prompt to be used.

### start vpn script

The `./start_vpn.sh` script is a small helper script designed to quickly start the uni vpn, allowing for work to be carried outside the uni campus.

It uses the `openfortivpn` command and my uni e-mail to start the vpn.

## Usage

All necessary command are launched using `just` command runner.

Command definitions are contained in `./justfile`.

Available commands with a brief documentation can be listed running:

```sh
just
```

The following lists the available commands describing them.

### default

Runs when providing no params to `just` command.
Lists available commands with a brief description.

### run

The `just run` command launches the experiment with the configuration in `maze_solver/src/experiment/config.py` and saves the result in the `results` directory.
Being the experiment run expected to be a computationally intensive command, it is thought to be executed on a server (with the helper script `run.sh`).

### stats

The `just stats` command can be called with 4 subcommands:

- \<experiment_date\>: print stats for give experiment
- last: print stats of last experiment
- list: list available experiment dates
- help: print help message

where \<experiment_date\> is a valid date in the format `yyyy-mm-dd_hh:mm:ss`, present in the `results` directory.

### render

The `just render <path-to-run> [output-file]` command renders a run into a mp4 file, to allow for it to be easily shared and stored. The \[output-file\] is optional, if not provided the file is saved in the project root folder with name `maze_run.mp4`.
Path to run must be a valid path to a run. An example path is: `results/2025-11-12_16:49:33/llama3/3x3/0.yaml`

### chat

The `just chat` command is meant to test prompt engineering approaches locally and interactively, without the need to run an actual test.
The configuration for the interactive chat is in the `./chat` directory.

The `./chat` directory contains the following files:

- `config.yaml`: where the model to be used is configured.
- `system_prompt.txt`: where the system_prompt for the chat exchange (used only once) is configured
- `prompt.txt`: where the prompt is read for every step. This file is meant to be changed every step with the new step prompt to be used.

### test

The `just test <test_name>` command provides a way to quickly test functionalities of the python source. The \<test_name\> must be a valid file name (with or without the `.py` extension) present in the `maze_solver/src/test` directory. These files define a `run()` method to be executed when that test is run. This allows to quickly iterate over development functionalities without the need to run a full experiment (`just run` command) to test them out.

### visualize

The `just visualize` command opens a new web broser page with the `maze_solver/src/visualize.ipynb` jupyter notebook. This notebook allows to visualize interactively (with a step count slider) a given run. This is used to check out the experiment results in more detail that simply printing the experiment stats with the `just stats` command.

### copy

The `just copy` command uses the `rsync` command to copy the contents of the results directory on the university `raptor1` server to the local results directory. This is commonly done, in the intended development workflow, when a new experiment finished running on the server and should be copied locally to review it's results.

### generate

The `just generate` command generates all the figures used in the master thesis, saving the to the `./figures/` directory.
Being them generated files, they are ignored by the repo.

### add

The `just add [library]` command allows to add python library dependencies to the project using uv, where \[library\] is the name of the python package, as one would pass it to the `pip` or `uv add` commands.

### remove

The `just remove [library]` command allows to remove python library dependencies to the project using uv, where \[library\] is the name of the python package, as one would pass it to the `pip -u` or `uv remove` commands.

## Workflow

The intended workflow, as of the current project structure is as follows:

- New functionality is developed, and a small test is created in `maze_solver/src/test/` directory, ran using `just test [test_name]` command.
- Experiments are run on the server using the `run.sh` script, defining the configuration for each experiment in the `maze_solver/src/experiment/config.py` file.
- Once the experiment is executed it is copied locally with the `just copy` command
- It's stats are printed using `just stats last` command.
- It's single runs are observed using `just visualize` command.
- Interesting runs are rendered using `just render [path_to_run]` command.
- Quick prompt engineering tests are carried using the interactive chat provided by the `just chat` command.
- python dependencies are managed using the `just add [library]` and `just remove [library]`
