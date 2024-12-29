"""
Day 22: Monkey Market

https://adventofcode.com/2024/day/22
"""

import logging
import pathlib

import duckdb

from advent_of_code.meta import read_input

HERE = pathlib.Path(__file__).parent


def _read(file: str) -> str:
    """
    Read the file.
    """
    return (HERE / file).read_text("utf-8")


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 22 problem!
    """
    if use_sample:
        part_1_file = str((HERE / "sample-1.data").absolute())
        part_2_file = str((HERE / "sample-2.data").absolute())
    else:
        input_data = HERE / "input.data"
        part_1_file = str(input_data.absolute())
        part_2_file = part_1_file
        read_input(input_data)

    part_1 = _read("part-1.sql").replace("{{ file }}", part_1_file)
    part_2 = _read("part-2.sql").replace("{{ file }}", part_2_file)

    return [
        duckdb.sql(part_1).fetchone()[0],
        duckdb.sql(part_2).fetchone()[0],
    ]
