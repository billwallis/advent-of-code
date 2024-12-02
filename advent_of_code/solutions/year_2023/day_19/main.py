"""
Day 19: Aplenty

https://adventofcode.com/2023/day/19
"""

from __future__ import annotations

import logging
import pathlib

from advent_of_code.meta import read_input


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 19 problem!
    """
    logging.basicConfig(level="DEBUG")
    file = "sample.data" if use_sample else "input.data"
    input_ = read_input(pathlib.Path(__file__).parent / file)

    return [
        0,
        0,
    ]
