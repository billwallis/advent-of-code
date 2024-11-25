"""
OOP solution for day 3.
"""

import warnings
from typing import Any

import advent_of_code.year_2022.day_03.constants as constants


def get_priority(item: str) -> int:
    """
    Get the priority for the corresponding item.
    """
    return constants.PRIORITY[item]


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


class Group:
    """
    A group of 3 rucksacks.
    """

    def __init__(self, rucksacks: list[Rucksack]):
        if (length := len(rucksacks)) != 3:
            warnings.warn(f"Expected 3 Rucksacks, found {length}")

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


class Rucksacks:
    """
    A collection of Rucksacks.
    """

    def __init__(self, all_contents: str):
        self.all_contents = all_contents
        self.rucksacks = [Rucksack(contents) for contents in all_contents.split("\n")]
        self.groups = [
            Group(self.rucksacks[3 * i : 3 * (i + 1)])
            for i in range(len(self.rucksacks) // 3)
        ]

    def sum_shared_item_priorities(self) -> int:
        """
        Sum the priority of the items shared between the compartments.
        """
        return sum(
            get_priority(rucksack.find_shared_item()) for rucksack in self.rucksacks
        )

    def sum_group_item_priorities(self) -> int:
        """
        Sum the priority of the items (badges) shared within the groups.
        """
        return sum(get_priority(group.find_badge()) for group in self.groups)


def solution(input_: str) -> list[Any]:
    """
    Solve the day 3 problem!
    """
    rucksacks = Rucksacks(input_.strip())

    return [
        rucksacks.sum_shared_item_priorities(),
        rucksacks.sum_group_item_priorities(),
    ]
