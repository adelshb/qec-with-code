![Logo](qec-with-code_logo.png)

[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue)](https://opensource.org/licenses/Apache-2.0)

This repository provides a collection of **Quantum Error Correction (QEC)** code implementations. The goal is to demonstrate how QEC works with different error thresholds and provide practical examples of implementing error correction codes on quantum circuits.

## List of Implemented QEC Codes

- **[Repetition code](notebooks/repetition_code.ipynb)**
- **[Rotated surface code](notebooks/rotated_surface_code.ipynb)**

## Installation

This package can be installed by cloning the repository and running

```console
pip install .
```

in the root directory of this repostory.
To install in editable mode with the optional dependencies required for development, run

```console
pip install -e ".[dev]"
```

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

## License
**[Apache License 2.0](LICENSE)**
