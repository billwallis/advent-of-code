"""
Tests for the Advent of Code solutions.
"""

from typing import Any

import pytest
import yaml

from advent_of_code import Solution
from advent_of_code.constants import SOLUTIONS_ROOT

# year-00: day-00: sample/actual: part-0: value
Solutions = dict[str : dict[str : dict[str : dict[str:Any]]]]

SKIP = [
    (2022, 5),
    (2022, 17),
    (2023, 5),
]


def _parse_date_key(date_string: str) -> int:
    return int(date_string.split("-")[1])


def _sample_solutions() -> Solutions:
    solutions_text = (SOLUTIONS_ROOT / "solutions.yaml").read_text("utf-8")
    solutions = yaml.load(
        stream=solutions_text,
        Loader=yaml.FullLoader,  # noqa: S506
    )
    return solutions["solutions"]


def _year_day_parts(solutions: Solutions) -> list[tuple[int, int, dict]]:
    """
    The year and day for the solution.
    """
    cases = []
    for year, days in solutions.items():
        for day, sample_or_actual in days.items():
            cases.append(
                (
                    _parse_date_key(year),
                    _parse_date_key(day),
                    sample_or_actual["sample"],
                )
            )
    return cases


@pytest.mark.parametrize(
    "year, day, parts",
    _year_day_parts(_sample_solutions()),
)
def test__sample_solutions(year: int, day: int, parts: dict):
    """
    Test that the solutions work for the sample inputs.
    """
    if (year, day) in SKIP:
        pytest.skip()
        return

    try:
        solution = Solution(day, year)
    except ModuleNotFoundError:
        pytest.skip()
        return

    actual = solution.solve(use_sample=True)
    assert actual[0] == parts["part-1"]
    assert actual[1] == parts["part-2"]
