"""
OOP solution for day 4.
"""

from __future__ import annotations

from typing import Any


class Assignment:
    """
    A section assignment.

    This is a range between section IDs, such as ``2-4`` (which means that the
    section assignment is 2, 3, and 4).
    """

    def __init__(self, lower_id: int | str, upper_id: int | str):
        self.lower_id = min(int(lower_id), int(upper_id))
        self.upper_id = max(int(lower_id), int(upper_id))

    def __str__(self):
        return f"{self.lower_id:02d}-{self.upper_id:02d}"

    def __repr__(self):
        return f"Assignment({self.lower_id=}, {self.upper_id=})"

    def __contains__(self, other: Assignment | int):
        """
        Emulate the ``set.issubset()`` method for ``Assignment``s.

        An ``Assignment`` object is in another if its section assignment range
        is fully contained in the other's. Additionally, an integer is in an
        ``Assignment`` if it is within the assignment's range.

            >>> assignment_1 = Assignment(2, 4)
            >>> assignment_2 = Assignment(1, 5)
            >>> assignment_1 in assignment_2
            True
            >>> assignment_2 in assignment_1
            False
            >>> 3 in assignment_1
            True
        """
        match other:
            case Assignment():
                return (
                    self.lower_id >= other.lower_id and self.upper_id <= other.upper_id
                )
            case int():
                return self.lower_id <= other <= self.upper_id

    def overlaps(self, other: Assignment) -> bool:
        """
        Return ``True`` if the assignments have at least 1 overlapping section.

        Note that 'overlaps' is a bidirectional property: that is, given two
        assignments ``A`` and ``B``, then ``A`` overlaps ``B`` if and only if
        ``B`` overlaps ``A``. Progmmatically, this means that ``A.overlaps(B) ==
        B.overlaps(A)``.

            >>> assignment_1 = Assignment(2, 3)
            >>> assignment_2 = Assignment(3, 4)
            >>> assignment_3 = Assignment(4, 5)
            >>> assignment_1.overlaps(assignment_2)
            True
            >>> assignment_1.overlaps(assignment_3)
            False
        """
        return (
            self.lower_id <= other.lower_id <= self.upper_id
            or self.lower_id <= other.upper_id <= self.upper_id
            or other.lower_id <= self.lower_id <= other.upper_id
            or other.lower_id <= self.upper_id <= other.upper_id
        )

    @classmethod
    def from_hyphenated_range(cls, hyphenated_range: str) -> Assignment:
        """
        Create an ``Assignment`` from a string hyphenated range.

        For example, the hyphenated range ``2-4`` is the following
        ``Assignment``::

            Assignment(lower_id=2, upper_id=4)
        """
        lower_id, upper_id = hyphenated_range.split("-")
        return cls(lower_id=lower_id, upper_id=upper_id)


class AssignmentPair:
    """
    A section assignment pair.
    """

    def __init__(self, assignment_1: Assignment, assignment_2: Assignment):
        self.assignment_1 = assignment_1
        self.assignment_2 = assignment_2

    def __str__(self):
        return f"{self.assignment_1},{self.assignment_2}"

    def __repr__(self):
        return f"AssignmentPair({self.assignment_1=}, {self.assignment_2=})"

    def is_one_range_fully_contained(self) -> bool:
        """
        Check whether either of the assignments are fully contained in the
        other.
        """
        return (
            self.assignment_1 in self.assignment_2
            or self.assignment_2 in self.assignment_1
        )

    def do_ranges_overlap(self) -> bool:
        """
        Check whether the assignments overlap.
        """
        return self.assignment_1.overlaps(self.assignment_2)

    @classmethod
    def from_comma_delimited_pair(cls, comma_delimited_pair: str) -> AssignmentPair:
        """
        Create an ``AssignmentPair`` from a comma delimited pair.

        For example, the comma delimited pair ``2-4,6-8`` is the following
        ``AssignmentPair``::

            AssignmentPair(
                assignment_1=Assignment(lower_id=2, upper_id=4),
                assignment_2=Assignment(lower_id=6, upper_id=8),
            )
        """
        assignment_1, assignment_2 = comma_delimited_pair.split(",")
        return cls(
            assignment_1=Assignment.from_hyphenated_range(assignment_1),
            assignment_2=Assignment.from_hyphenated_range(assignment_2),
        )


class AssignmentPairs:
    """
    A collection of ``AssignmentPair`` objects.
    """

    def __init__(self, assignment_pairs: str):
        self._assignment_pairs = assignment_pairs
        self.assignment_pairs = [
            AssignmentPair.from_comma_delimited_pair(pair)
            for pair in assignment_pairs.split("\n")
        ]

    def __iter__(self):
        yield from self.assignment_pairs

    def get_number_of_fully_contained_assignments(self) -> int:
        """
        Return the number of assignment pairs that have an assignment fully
        contained in the other.
        """
        return sum(
            int(assignment_pair.is_one_range_fully_contained())
            for assignment_pair in self
        )

    def get_number_of_overlaps(self) -> int:
        """
        Return the number of assignment pairs that overlap in at least 1
        section.
        """
        return sum(int(assignment_pair.do_ranges_overlap()) for assignment_pair in self)


def solution(input_: str) -> list[Any]:
    """
    Solve the day 4 problem!
    """
    assignment_pairs = AssignmentPairs(input_.strip())

    return [
        assignment_pairs.get_number_of_fully_contained_assignments(),
        assignment_pairs.get_number_of_overlaps(),
    ]
