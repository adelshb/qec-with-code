# Contributing

## Installation (for developers)

This package can be installed by cloning the repository and to install in editable mode with the optional dependencies required for development, run

```console
pip install -e ".[dev]"
```

## How to contribute

### Find an issue

Start by looking at the issue list (more to come). If you don't know where to start look for the tag "good first issue". Then make your interest public and one of the lead developers will come back to you and assign you the issue if it is available and still relevant.

### Work on the issue

You can fork the repository on your own account. Then create a branch and work on the issue. Once you are ready you can submit a PR on the main branch. Please provide as much information as possible to help the reviewer.

Please make sure to also include tests in your submission. For details about running tests see the section below.

## Running tests with pytest

The repository contains a tests folder which mimics the architecture of the code, each file and method and attributes must be tested as much as possible.

To run tests without collecting test coverage data, you can simply use the following command:

```console
pytest
```

in the root directory of this repostory.
If you want a more detailed coverage report in the terminal,  you can simply use the following command:

```console
pytest tests --cov --cov-report term-missing
```
