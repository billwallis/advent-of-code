"""
Advent of Code!

https://adventofcode.com/
"""

import advent_of_code.solutions
import advent_of_code.utils


def main() -> None:
    """
    Print the solutions.
    """
    # advent_of_code.utils.create_files(year=2023, day=None)

    advent_of_code.solutions.print_solutions(
        print_all=False,
        year=2023,
        # print_day=1,
    )


if __name__ == "__main__":
    main()
