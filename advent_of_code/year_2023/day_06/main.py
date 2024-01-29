"""
Solution for day 6.
"""

from __future__ import annotations

import dataclasses
import logging
import math
from typing import Any


def _travel(max_time: int, time: int, acceleration: int) -> int:
    """
    Return the distance travelled in ``max_time`` milliseconds where the
    ``acceleration`` is applied for ``time`` milliseconds.

    No distance is travelled while the acceleration is applied.

    :param max_time: The maximum time in travel (milliseconds).
    :param time: The time to apply the acceleration (milliseconds).
    :param acceleration: The acceleration (millimeters/milliseconds).
    """
    assert 0 <= time <= max_time

    speed = acceleration * time

    return speed * (max_time - time)


def _number_of_ints_between(_min: float, _max: float, /) -> int:
    """
    Return the number of integers between ``min_`` and ``max_``, exclusive.
    """
    min_, max_ = sorted([_min, _max])

    return math.ceil(max_) - math.floor(min_) - 1


def solve_time_from_distance(time: int, distance: int, acceleration: int) -> int:
    """
    Given a ``time``, ``distance``, and ``acceleration``, return the number
    of integer times that would exceed the ``distance`` travelled in ``time``
    using the logic of the ``travel`` function above.
    """
    # We simply need to solve the equation below for `x`:
    #
    #   distance < acceleration * x * (time - x)
    #
    # ...and then count the number of integer solutions.
    quadratic_root = math.sqrt((time**2) - (4 * distance / acceleration))
    x_1, x_2 = (time - quadratic_root) / 2, (time + quadratic_root) / 2

    logging.debug(
        f"Calculating roots for time {time}, distance {distance}, and"
        f" acceleration {acceleration}"
    )
    logging.debug(f"The roots of the quadratic are: {x_1:.4f}, {x_2:.4f}")

    return _number_of_ints_between(x_1, x_2)


@dataclasses.dataclass
class Record:
    """
    A race record, which has a time and a distance.
    """

    time: int
    distance: int

    @classmethod
    def from_tuple(cls, time_distance: tuple) -> Record:
        """
        Create a ``Record`` from a tuple of time and distance.
        """
        return cls(time=time_distance[0], distance=time_distance[1])


class RaceRecord:
    """
    The record of best races, with a time and distance.
    """

    records: list[Record]

    def __init__(self, records: list[Record]) -> None:
        """
        Initialize the record.
        """
        self.records = records

    @classmethod
    def from_text(cls, text: str) -> RaceRecord:
        """
        Create a ``RaceRecord`` from a text representation.

        The text representation will look something like::

            Time:      7  15   30
            Distance:  9  40  200
        """

        def _parse(line: str) -> list[int]:
            return [int(x) for x in line.split(":")[-1].split()]

        time_text, distance_text = text.strip().splitlines()
        times, distances = _parse(time_text), _parse(distance_text)

        assert len(times) == len(distances)
        return cls(records=[Record.from_tuple(t_d) for t_d in zip(times, distances)])

    @property
    def margin_of_error(self) -> int:
        """
        Return the margin of error, which is the product of the number of ways
        you can beat the record in each race.
        """
        return math.prod(
            [
                solve_time_from_distance(
                    time=record.time,
                    distance=record.distance,
                    acceleration=1,
                )
                for record in self.records
            ]
        )


def solution(input_: str) -> list[Any]:
    """
    Solve the day 6 problem!
    """
    logging.basicConfig(level="INFO")

    race_record = RaceRecord.from_text(input_)
    race_record_adj = RaceRecord.from_text(input_.replace(" ", ""))

    return [
        race_record.margin_of_error,
        race_record_adj.margin_of_error,
    ]
