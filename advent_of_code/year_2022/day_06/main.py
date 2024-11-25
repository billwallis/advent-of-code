"""
OOP solution for day 6.
"""

from typing import Any


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
        self, number_of_distinct_characters: int
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


def solution(input_: str) -> list[Any]:
    """
    Solve the day 6 problem!
    """
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
