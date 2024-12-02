"""
Day 6: Tuning Trouble

https://adventofcode.com/2022/day/6
"""

import pathlib

from advent_of_code.meta import read_input


class DatastreamBuffer:
    """
    A datastream buffer, which is a signal of seemingly-random characters.
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"{self.message}"

    def __repr__(self):
        return f"DatastreamBuffer({self.message=})"

    def find_position_of_distinct_sequence(
        self,
        number_of_distinct_characters: int,
    ) -> int:
        """
        Find the first position where the preceding number of distinct
        characters are all unique.
        """
        number_adj = number_of_distinct_characters - 1
        for pos in range(len(self.message)):
            if (
                pos >= number_adj
                and len(set(self.message[pos - number_adj : pos + 1]))
                == number_of_distinct_characters
            ):
                # Python starts counting at 0, but AoC starts counting at 1
                return pos + 1
        raise ValueError("No distinct sequence found")


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 6 problem!
    """
    file = "sample.data" if use_sample else "input.data"
    input_ = read_input(pathlib.Path(__file__).parent / file)

    datastream_buffer = DatastreamBuffer(
        input_.strip().split("\n")[0]
    )  # Just to include the many sample inputs

    return [
        datastream_buffer.find_position_of_distinct_sequence(
            number_of_distinct_characters=4
        ),
        datastream_buffer.find_position_of_distinct_sequence(
            number_of_distinct_characters=14
        ),
    ]
