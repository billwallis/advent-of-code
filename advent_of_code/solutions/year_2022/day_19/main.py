"""
Day 19: Not Enough Minerals

https://adventofcode.com/2022/day/19
"""

import pathlib

from advent_of_code.meta import read_input


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 19 problem!
    """
    file = "sample.data" if use_sample else "input.data"
    input_ = read_input(pathlib.Path(__file__).parent / file)

    return [0, 0]
