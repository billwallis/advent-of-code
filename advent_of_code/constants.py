"""
Constants for Advent of Code.
"""

import pathlib

PROJECT_ROOT = pathlib.Path(
    __file__
).parent.parent  # Resolves to `advent-of-code/`
if PROJECT_ROOT.name != "advent-of-code":
    raise AssertionError("The project root is not 'advent-of-code'")

SOLUTIONS_ROOT = PROJECT_ROOT / "advent_of_code/solutions"
