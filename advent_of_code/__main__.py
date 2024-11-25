"""
Advent of Code!

https://adventofcode.com/
"""

import datetime

import arguably

import advent_of_code


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
        advent_of_code.print_solutions(
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
    advent_of_code.create_files(*_parse_year_and_day(year, day))


if __name__ == "__main__":
    arguably.run(name="advent_of_code")
