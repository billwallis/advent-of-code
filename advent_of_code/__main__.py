"""
Advent of Code!

https://adventofcode.com/
"""

import advent_of_code.solutions
import advent_of_code.utils


# TODO: Add a CLI so that we don't need to comment code in and out
def main() -> None:
    """
    Print the solutions.
    """
    # advent_of_code.utils.create_files(year=2024, day=1)

    advent_of_code.solutions.print_solutions(
        print_all=False,
        year=2024,
        print_day=1,
    )


if __name__ == "__main__":
    main()
