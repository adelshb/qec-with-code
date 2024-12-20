# QEC with Code

A library for testing Quantum Error Correction (QEC).

## List of implemented QEC

- [Repetition code](notebooks/repetition_code.ipynb)
- [Surface code](notebooks/surface_code.ipynb)

## Installation

This package can be installed by cloning the repository and running

```console
pip install .
```

in the root directory of this repostory.
To install in editable mode with the optional dependencies required for development, run

```console
pip install -e ".[dev,docs]"
```

## Documentation

TBA

## Running tests with pytest

To run tests without collecting test coverage data, you can simply use the following command:

```console
pytest
```

in the root directory of this repostory.
If you want a more detailed coverage report in the terminal,  you can simply use the following command:

```console
pytest tests --cov --cov-report term-missing
```

## Contributing
