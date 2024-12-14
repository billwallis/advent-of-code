"""
Create the template files for the daily problems.
"""

import pathlib

import jinja2

from advent_of_code.constants import SOLUTIONS_ROOT

HERE = pathlib.Path(__file__).parent


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
        self.directory = SOLUTIONS_ROOT / f"year_{year}/day_{day:02d}"

    def create_files(self) -> None:
        """
        Create the daily directory and its files.

        TODO: Merge with `aoc_website` to get the data from the website.
        """
        self.directory.mkdir(parents=True, exist_ok=True)
        (self.directory / "sample.data").touch()

        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(HERE / "template"),
            autoescape=True,
        )
        params = {
            "day": self.day,
            "year": self.year,
            "title": "[Problem title]",
        }

        main_file = template_env.get_template("main.py").render(**params)
        (self.directory / "main.py").write_text(main_file)

        part_file = template_env.get_template("part.sql").render(**params)
        (self.directory / "part-1.sql").write_text(part_file)
        (self.directory / "part-2.sql").write_text(part_file)


def create_files(year: int, day: int) -> None:
    """
    Create the template files for the day.
    """
    FileCreator(day=day, year=year).create_files()
