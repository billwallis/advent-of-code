<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![tests](https://github.com/Bilbottom/advent-of-code/actions/workflows/tests.yaml/badge.svg)](https://github.com/Bilbottom/advent-of-code/actions/workflows/tests.yaml)
[![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/advent-of-code)](https://shields.io/badges/git-hub-last-commit)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Bilbottom/advent-of-code/main.svg)](https://results.pre-commit.ci/latest/github/Bilbottom/advent-of-code/main)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)

</div>

---

# Advent of Code

Solutions to the Advent of Code problem sets, available at:

- [https://adventofcode.com/](https://adventofcode.com/)

This is just an opportunity for me to work on my OOP, so the solutions are not optimal.

## Quick start

This project uses:

- [Poetry](https://python-poetry.org/) for package management
- [pre-commit](https://pre-commit.com/) for linting
- [arguably](https://treykeown.github.io/arguably/) for the CLI

```shell
# Setup
poetry install --sync
pre-commit install --with-hooks

# Use the CLI
aoc --help
```

Create an `.env` file with the session cookie you get from Advent of Code:

```
AOC_SESSION_COOKIE="session=..."
```

You can find the session cookie in your browser's developer tools after logging in to Advent of Code.
