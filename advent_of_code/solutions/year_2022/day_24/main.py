"""
Day 24: Blizzard Basin

https://adventofcode.com/2022/day/24
"""

import pathlib

from advent_of_code.meta import read_input


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 24 problem!
    """
    file = "sample.data" if use_sample else "input.data"
    input_ = read_input(pathlib.Path(__file__).parent / file)

    return [0, 0]
