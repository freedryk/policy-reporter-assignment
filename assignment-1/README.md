# Assignment 1

This folder contains my solution for Assignment 1.

Input data is expected in JSONL file format with one JSON object per line in the format

```JSON
{"threshold": 0.1, "true_positive": 10, "false_positive": 5, "false_negative": 2, "true_negative": 8}
```

A test data file, [test.jsonl](test.jsonl), in included in this repository.

To determine the best threshold that achieves a recall >= 0.9, I filter all thresholds with recall less than 0.9,
then sort the remaining thresholds by their [f1 score](https://en.wikipedia.org/wiki/F-score).

## Running

This repository uses `uv` for package installation and management. uv installation instructions can be found
[here](https://docs.astral.sh/uv/getting-started/installation/).

The code can be installed and run via:
```bash
uv run assignment1.py
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

