"""
Day 20: Pulse Propagation

https://adventofcode.com/2023/day/20
"""

from __future__ import annotations

import logging
import pathlib

from advent_of_code.meta import read_input


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 20 problem!
    """
    logging.basicConfig(level="DEBUG")
    file = "sample-1.data" if use_sample else "input.data"
    input_ = read_input(pathlib.Path(__file__).parent / file)

    return [
        0,
        0,
    ]
