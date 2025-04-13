# Assignment 2

This folder contains my solution for Assignment 2.

The Finite State Machine base class `FSM` is located in
[state_machine.py](src/assignement2/state_machine.py), along with a `State` class.
Code that uses these classes to implement a mod 3 operation on a string of binary is
present in [main.py](src/assignment_2/main.py) and runnable from the
[assignment2.py](assignment2.py) script.

The class definitions uses pydantic type-checking to ensure input fields are sensible.

## Running

This repository uses `uv` for package installation and management. uv installation instructions can be found
[here](https://docs.astral.sh/uv/getting-started/installation/).

The code can be installed and run via:
```bash
uv run assignment2.py
```

## Tests

Unit tests can be run by installing the package:
```bash
uv pip install -e .
```

and then running:
```bash
uv run pytest
```

