"""
Day 19: Linen Layout

https://adventofcode.com/2024/day/19
"""

import pathlib

import duckdb

from advent_of_code.meta import read_input

HERE = pathlib.Path(__file__).parent


def _read(file: str) -> str:
    """
    Read the file.
    """
    return (HERE / file).read_text("utf-8")


def solution(use_sample: bool) -> list:
    """
    Solve the day 19 problem!
    """
    file = HERE / ("sample.data" if use_sample else "input.data")
    read_input(file)

    part_1 = _read("part-1.sql").replace("{{ file }}", str(file.absolute()))
    part_2 = _read("part-2.sql").replace("{{ file }}", str(file.absolute()))

    return [
        duckdb.sql(part_1).fetchone()[0],
        duckdb.sql(part_2).fetchone()[0],
    ]
