"""
Create the template files for the daily problems.
"""

import datetime
import pathlib
import textwrap

from advent_of_code.constants import ROOT


class FileCreator:
    """
    Create the template files for the daily problems.
    """

    day: int
    year: int
    directory: pathlib.Path

    def __init__(self, day: int, year: int):
        self.day = day
        self.year = year
        self.directory = ROOT / f"year_{year}/day_{day:02d}"

    def write_to_file(self, filename: str, contents: str) -> None:
        """
        Write the contents to a file.

        Creates the file if it doesn't already exist.
        """
        with open(self.directory / filename, "w+") as f:
            f.write(contents)

    def create_files(self) -> None:
        """
        Create the daily directory and all of its files.
        """
        self._create_directory()
        self._create_init()
        self._create_dunder_main()
        self._create_main()
        self._create_readme()
        self._create_data_files()

    def _create_directory(self) -> None:
        """
        Create the directory for the daily problem.
        """
        self.directory.mkdir(parents=True, exist_ok=True)

    def _create_init(self) -> None:
        """
        Create the ``__init__`` file for the daily problem.
        """
        self.write_to_file(
            filename="__init__.py",
            contents=textwrap.dedent(
                f'''\
                """
                Day {self.day}:

                https://adventofcode.com/{self.year}/day/{self.day}/input
                """
                from advent_of_code.year_{self.year}.day_{self.day:02d}.main import solution
                '''
            ),
        )

    def _create_dunder_main(self) -> None:
        """
        Create the ``__main__`` file for the daily problem.
        """
        self.write_to_file(
            filename="__main__.py",
            contents=textwrap.dedent(
                f"""\
                import pathlib

                from advent_of_code.year_{self.year}.day_{self.day:02d}.main import solution

                if __name__ == "__main__":
                    sample = pathlib.Path(__file__).parent / "sample.data"
                    print(solution(input_=sample.read_text().strip()))
                """
            ),
        )

    def _create_main(self) -> None:
        """
        Create the main file for the daily problem.
        """
        self.write_to_file(
            filename="main.py",
            contents=textwrap.dedent(
                f'''\
                """
                Solution for day {self.day}.
                """
                from __future__ import annotations

                import logging
                from typing import Any


                def solution(input_: str) -> list[Any]:
                    """
                    Solve the day {self.day} problem!
                    """
                    logging.basicConfig(level="DEBUG")

                    return [
                        0,
                        0,
                    ]
                '''
            ),
        )

    def _create_readme(self) -> None:
        """
        Create the readme file for the daily problem.
        """
        self.write_to_file(
            filename="README.md",
            contents=textwrap.dedent(
                f"""\
                --- Day {self.day}:  ---

                ### Part One


                ### Part Two

                """
            ),
        )

    def _create_data_files(self) -> None:
        """
        Create the data files for the daily problem.
        """
        self.write_to_file(filename="sample.data", contents="")
        self.write_to_file(filename="input.data", contents="")


def create_files(year: int, day: int = None) -> None:
    """
    Create the template files for the day.
    """
    day_ = day or datetime.datetime.now().day
    FileCreator(day=day_, year=year).create_files()
