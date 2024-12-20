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

## Testing

This project uses [pytest](https://docs.pytest.org/en/stable/) for unit tests.
Tests can be run by running

```console
pytest
```

in the root directory of this repostory.
A coverage report produced using the following arguments:

```console
pytest tests --cov --cov-report term-missing
```

## Contributing
