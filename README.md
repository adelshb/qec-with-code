# QEC with Code

This repository provides a library of **Quantum Error Correction (QEC)** code implementations using **Stim**. The goal is to demonstrate how QEC works with different error thresholds and provide practical examples of implementing error correction codes on quantum circuits.

### Overview

Quantum computers are highly susceptible to errors due to noise and decoherence. **Quantum Error Correction (QEC)** aims to mitigate these errors and make quantum computers more reliable. In this project, we showcase the implementation of QEC using **Stim**, a simulator designed for quantum error correction, and **Pymatching**, a Python library for decoding error syndromes.

This project is designed to provide:
- **Examples of QEC implementation**: Real-world examples of how quantum error correction codes are used to correct errors in quantum circuits.
- **Threshold analysis**: Demonstrations of how QEC codes' performance varies with different error thresholds or noise levels.
- **Integration with Stim and Pymatching**: A practical guide on how to utilize **Stim** for simulating error correction and **Pymatching** for decoding.

## List of Implemented QEC Codes

- **[Repetition code](notebooks/repetition_code.ipynb)**: A simple example of a 1D repetition code implemented for error correction.
- **[Surface code](notebooks/surface_code.ipynb)**: An implementation of the 2D surface code, one of the most well-known error correction codes in quantum computing.


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

TBA