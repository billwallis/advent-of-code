"""
Parsers for the Advent of Code website.
"""

import os
import pathlib

import dotenv
import requests

dotenv.load_dotenv()


def _get_input(year: int, day: int) -> str:
    """
    Get the input for the given day and year.
    """
    return requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        headers={"Cookie": os.environ["AOC_SESSION_COOKIE"]},
        timeout=10,
    ).text


def _parse_year_and_day(path: pathlib.Path) -> tuple[int, int]:
    """
    Parse the year and day from the path.

    The path should be in the form of `year/day`.
    """
    try:
        day = path.parent.name
        year = path.parent.parent.name
        return int(year[-4:]), int(day[-2:])
    except ValueError:
        raise ValueError(
            f"Path '{path}' is not in the form '.../year_0000/day_00/file.ext'."
        )


def read_input(path: pathlib.Path) -> str:
    """
    Open the file and return its contents.

    If the file is the input file and doesn't yet exist at the location, it
    will be read from the website.
    """
    if not path.exists():
        if path.name == "input.data":
            text = _get_input(*_parse_year_and_day(path))
            path.write_text(text)
            return text.strip()
        raise FileNotFoundError(f"File '{path}' not found.")
    return path.read_text().strip()
