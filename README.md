![Logo](qec-with-code_logo.png)

[![Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue)](https://opensource.org/licenses/Apache-2.0)

This repository provides a collection of **Quantum Error Correction (QEC)** code implementations using **Stim**. The goal is to demonstrate how QEC works with different error thresholds and provide practical examples of implementing error correction codes on quantum circuits.

### Overview

Quantum computers are highly susceptible to errors due to noise and decoherence. **Quantum Error Correction (QEC)** aims to mitigate these errors and make quantum computers more reliable. In this project, we showcase the implementation of QEC using **Stim**, a simulator designed for quantum error correction, and **Pymatching**, a Python library for decoding error syndromes.

This project is designed to provide:
- **Examples of QEC implementation**: Real-world examples of how quantum error correction codes are used to correct errors in quantum circuits.
- **Threshold analysis**: Demonstrations of how QEC codes' performance varies with different error thresholds or noise levels.
- **Integration with Stim and Pymatching**: A practical guide on how to utilize **Stim** for simulating error correction and **Pymatching** for decoding.

## List of Implemented QEC Codes

- **[Repetition code](notebooks/repetition_code.ipynb)**: A simple example of a 1D repetition code implemented for error correction.
- **[Rotated surface code](notebooks/rotated_surface_code.ipynb)** (TBA): An implementation of the 2D surface code, one of the most well-known error correction codes in quantum computing.


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

## How to Contribute

We welcome contributions to this project! To get started, please follow these steps:

### 1. Fork the Repository
Click the **Fork** button in the top-right corner of the repository page to create a copy of the repository in your GitHub account.

### 2. Create a New Branch
Create a new branch for your changes. This keeps your work separate from the main codebase.

```console
git checkout -b my-feature-branch
```

### 3. Make Your Changes
Work on your changes locally. Make sure to follow the project’s coding conventions, and keep your changes focused on a single task or issue.

### 4. Commit Your Changes
Once you're happy with your changes, commit them with a clear and concise message describing what you’ve done.

```console
git add .
git commit -m "Add feature XYZ"
```

### 5. Sync Your Fork
Before pushing, ensure your fork is up-to-date with the latest changes from the main repository:

```console
git fetch upstream
git rebase upstream/main
```

### 6. Push Your Changes
Push your changes to your fork on GitHub.

```console
git push origin my-feature-branch
```

### 7. Create a Pull Request
Open a pull request (PR) from your fork’s branch to the main repository. Provide a clear description of what you've done and reference any related issues (e.g., "Fixes #123").

### 8. Engage in the Review Process
Our maintainers will review your pull request. Be open to feedback and willing to make changes if necessary.

### 9. Stay Involved
Even after your PR is merged, we encourage you to stay involved and contribute to the project by reporting bugs, submitting more features, or helping with documentation!


## License
**[Apache License 2.0](LICENSE)**