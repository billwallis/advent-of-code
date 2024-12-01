"""
Parsers for the Advent of Code website.
"""

import os

import dotenv
import requests

dotenv.load_dotenv()


def get_input(day: int, year: int) -> str:
    """
    Get the input for the given day and year.
    """
    return requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        headers={"Cookie": os.environ["AOC_SESSION_COOKIE"]},
        timeout=10,
    ).text
