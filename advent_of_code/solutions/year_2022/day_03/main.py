"""
Day 3: Rucksack Reorganization!

https://adventofcode.com/2022/day/3
"""

import pathlib
import warnings

from advent_of_code.meta import read_input

GROUP_RUCKSACK_SIZE = 3
PRIORITY = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
    "A": 27,
    "B": 28,
    "C": 29,
    "D": 30,
    "E": 31,
    "F": 32,
    "G": 33,
    "H": 34,
    "I": 35,
    "J": 36,
    "K": 37,
    "L": 38,
    "M": 39,
    "N": 40,
    "O": 41,
    "P": 42,
    "Q": 43,
    "R": 44,
    "S": 45,
    "T": 46,
    "U": 47,
    "V": 48,
    "W": 49,
    "X": 50,
    "Y": 51,
    "Z": 52,
}


def get_priority(item: str) -> int:
    """
    Get the priority for the corresponding item.
    """
    return PRIORITY[item]


class Rucksack:
    """
    An elf's rucksack, consisting of items across 2 compartments.
    """

    def __init__(self, contents: str):
        self.contents = contents
        self.compartments = (
            contents[: len(contents) // 2],
            contents[len(contents) // 2 :],
        )

    def __repr__(self):
        return f"Rucksack({self.contents=}, {self.compartments=})"

    def find_shared_item(self) -> str:
        """
        Find the item shared between the compartments.
        """
        for item_1 in self.compartments[0]:
            for item_2 in self.compartments[1]:
                if item_1 == item_2:
                    return item_1
        raise ValueError("No shared item found")


class Group:
    """
    A group of 3 rucksacks.
    """

    def __init__(self, rucksacks: list[Rucksack]):
        if (length := len(rucksacks)) != GROUP_RUCKSACK_SIZE:
            warnings.warn(
                f"Expected {GROUP_RUCKSACK_SIZE} Rucksacks, found {length}"
            )

        self.rucksacks = rucksacks

    def find_badge(self) -> str:
        """
        Find the item shared between the compartments.
        """
        for item_1 in self.rucksacks[0].contents:
            for item_2 in self.rucksacks[1].contents:
                if item_1 == item_2:
                    for item_3 in self.rucksacks[2].contents:
                        if item_1 == item_3:
                            return item_1
        raise ValueError("No shared item found")


class Rucksacks:
    """
    A collection of Rucksacks.
    """

    def __init__(self, all_contents: str):
        self.all_contents = all_contents
        self.rucksacks = [
            Rucksack(contents) for contents in all_contents.split("\n")
        ]
        self.groups = [
            Group(self.rucksacks[3 * i : 3 * (i + 1)])
            for i in range(len(self.rucksacks) // 3)
        ]

    def sum_shared_item_priorities(self) -> int:
        """
        Sum the priority of the items shared between the compartments.
        """
        return sum(
            get_priority(rucksack.find_shared_item())
            for rucksack in self.rucksacks
        )

    def sum_group_item_priorities(self) -> int:
        """
        Sum the priority of the items (badges) shared within the groups.
        """
        return sum(get_priority(group.find_badge()) for group in self.groups)


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 3 problem!
    """
    file = "sample.data" if use_sample else "input.data"
    input_ = read_input(pathlib.Path(__file__).parent / file)

    rucksacks = Rucksacks(input_.strip())

    return [
        rucksacks.sum_shared_item_priorities(),
        rucksacks.sum_group_item_priorities(),
    ]
