"""
Solutions to the advent of code 2022 problems.
"""
import datetime
import functools
import importlib

import advent_of_code.utils


class Solution:
    """
    Programmatically grab the functions and object corresponding to the day's
    problems and solutions.

    Expects there to be a module called ``day_i`` with ``i`` replaced by the day
    number, which has the following properties:

    - ``SAMPLE_INPUT``: The sample input for the problem.
    - ``solution_oop``: The OOP version of the solution.
    - ``solution_optimal``: The optimal (?) version of the solution.
    """

    def __init__(self, year: int, day: int):
        self.day = day
        self.module = importlib.import_module(f"advent_of_code.year_{year}.day_{day}")
        self.oop_solution = getattr(self.module, "solution_oop")
        self.optimal_solution = getattr(self.module, "solution_optimal")

    def read_input(self, use_sample: bool) -> str:
        """
        Open the input file and return its contents.
        """
        if use_sample:
            return getattr(self.module, "SAMPLE_INPUT")

        return advent_of_code.utils.read_input(f"day_{self.day}")

    def print_solution(
        self, use_sample: bool, profile_solutions: bool = False, repeat: int = 10_000
    ) -> None:
        """
        Print the day's solution!
        """
        input_ = self.read_input(use_sample=use_sample)

        print(f"--- Day {self.day:02d} Solution ---")
        print(self.oop_solution(input_=input_))
        print(self.optimal_solution(input_=input_))
        print()

        if profile_solutions:
            advent_of_code.utils.profile(
                oop_solution=functools.partial(self.oop_solution, input_=input_),
                optimal_solution=functools.partial(
                    self.optimal_solution, input_=input_
                ),
                repeat=repeat,
            )


def print_all_solutions(
    print_all: bool,
    use_sample: bool,
    year: int,
    profile_solutions: bool = False,
    repeat: int = 10_000,
    print_day: int = None,
) -> None:
    """
    Print the solutions.
    """
    day_today = print_day or datetime.datetime.now().day

    if print_all:
        for i in range(day_today):
            sol = Solution(year=year, day=i + 1)
            sol.print_solution(
                use_sample=use_sample,
                profile_solutions=profile_solutions,
                repeat=repeat,
            )
    else:
        sol = Solution(year=year, day=day_today)
        sol.print_solution(
            use_sample=use_sample,
            profile_solutions=profile_solutions,
            repeat=repeat,
        )
