<span align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![tests](https://github.com/billwallis/advent-of-code/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/advent-of-code/actions/workflows/tests.yaml)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/advent-of-code/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/advent-of-code/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/advent-of-code)](https://shields.io/badges/git-hub-last-commit)

</span>

---

# Advent of Code

Solutions to the Advent of Code problem sets, available at:

- [https://adventofcode.com/](https://adventofcode.com/)

This is just an opportunity for me to work on my OOP, so the solutions are not optimal.

## Quick start

This project uses:

- [uv](https://docs.astral.sh/uv/getting-started/installation/) for package management
- [pre-commit](https://pre-commit.com/) for linting
- [arguably](https://treykeown.github.io/arguably/) for the CLI

```shell
# Setup
uv sync --all-groups
pre-commit install --with-hooks

# Use the CLI
aoc --help
```

Create an `.env` file with the session cookie you get from Advent of Code:

```
AOC_SESSION_COOKIE="session=..."
```

You can find the session cookie in your browser's developer tools after logging in to Advent of Code.
