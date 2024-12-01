"""
Advent of Code!

https://adventofcode.com/
"""

import datetime
import importlib
import os
import pathlib
from collections.abc import Callable
from typing import Any

import arguably

from advent_of_code import meta
from advent_of_code.constants import PROJECT_ROOT, SOLUTIONS_ROOT


class Solution:
    """
    Programmatically grab the functions and object corresponding to the
    day's problems and solutions.

    Expects there to be a module called ``day_i`` with ``i`` replaced by the
    day number which exposes a ``solution`` function.
    """

    day: int
    year: int
    path: pathlib.Path
    solution: Callable[[str], list[Any]]

    def __init__(self, day: int, year: int) -> None:
        """
        Get the files for the day's solution.
        """
        self.day = day
        self.year = year
        self.path = SOLUTIONS_ROOT / f"year_{year}/day_{day:02d}"

        module_path = self.path.relative_to(PROJECT_ROOT) / "main"
        module = importlib.import_module(
            str(module_path).replace(os.sep, "."),
            str(PROJECT_ROOT),
        )
        self.solution = getattr(module, "solution")

    def read_input(self) -> str:
        """
        Open the input file and return its contents.
        """
        input_path = self.path / "input.data"
        if not input_path.exists():
            text = meta.get_input(self.day, self.year)
            input_path.write_text(text)
            return text.strip()
        return input_path.read_text().strip()

    def print_solution(self) -> None:
        """
        Print the day's solution!
        """
        print(f"--- Year {self.year} Day {self.day:02d} Solution ---")
        print(self.solution(self.read_input()), "\n", sep="")


def print_solutions(print_all: bool, year: int, day: int) -> None:
    """
    Print the solutions.
    """
    if print_all:
        for i in range(day):
            Solution(year=year, day=i + 1).print_solution()
    else:
        Solution(year=year, day=day).print_solution()


def _parse_year_and_day(year: int | None, day: int | None) -> tuple[int, int]:
    today = datetime.date.today()
    return (
        year or today.year,
        day or today.day,
    )


@arguably.command
def __root__(
    *,
    year: int | None = None,
    day: int | None = None,
    print_all: bool = False,
) -> None:
    """
    Print the solutions.
    """
    if arguably.is_target():
        print_solutions(
            print_all,
            *_parse_year_and_day(year, day),
        )


@arguably.command
def create(
    *,
    year: int | None = None,
    day: int | None = None,
) -> None:
    """
    Create the daily files.
    """
    meta.create_files(*_parse_year_and_day(year, day))


if __name__ == "__main__":
    arguably.run(name="advent_of_code")
