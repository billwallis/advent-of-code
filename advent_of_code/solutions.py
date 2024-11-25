"""
Solutions to the Advent of Code problems.
"""

import datetime
import importlib
import os
import pathlib
import types
from typing import Callable

from advent_of_code.constants import ROOT


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
    module: types.ModuleType
    solution: Callable

    def __init__(self, day: int, year: int):
        self.day = day
        self.year = year
        self.path = ROOT / f"year_{year}/day_{day:02d}"
        self.module = importlib.import_module(
            str("advent_of_code" / self.path.relative_to(ROOT)).replace(os.sep, "."),
            str(ROOT),
        )
        self.solution = getattr(self.module, "solution")

    def read_input(self) -> str:
        """
        Open the input file and return its contents.
        """
        return (self.path / "input.data").read_text().strip()

    def print_solution(self) -> None:
        """
        Print the day's solution!
        """
        print(f"--- Year {self.year} Day {self.day:02d} Solution ---")
        print(self.solution(input_=self.read_input()), "\n", sep="")


def print_solutions(
    print_all: bool,
    year: int,
    print_day: int = None,
) -> None:
    """
    Print the solutions.
    """
    day_today = print_day or datetime.date.today().day

    if print_all:
        for i in range(day_today):
            Solution(year=year, day=i + 1).print_solution()
    else:
        Solution(year=year, day=day_today).print_solution()
