"""
Solution for day 3.
"""

from __future__ import annotations

import collections
import copy
import dataclasses
import functools
import logging
import pathlib
from typing import Generator

import advent_of_code.utils.geometry


# noinspection DuplicatedCode
class Position(advent_of_code.utils.geometry.Position):
    """
    A position on a 2-dimensional plane of integers.
    """

    @property
    def neighbours(self) -> list[Position]:
        """
        Return the positions of the 8 immediate neighbours of the current
        position.
        """
        return [
            self + direction
            for direction in [
                UP,
                DOWN,
                LEFT,
                RIGHT,
                UP + LEFT,
                UP + RIGHT,
                DOWN + LEFT,
                DOWN + RIGHT,
            ]
        ]


# noinspection DuplicatedCode
# Math co-ordinates
ZERO = Position(0, 0)
UP = Position(0, 1)
DOWN = Position(0, -1)
LEFT = Position(-1, 0)
RIGHT = Position(1, 0)


class Token:
    """
    A token in the engine schematic.
    """

    token: str
    is_digit: bool
    is_symbol: bool

    def __init__(self, token: str):
        self.token = token
        self.is_digit = token.isdigit()
        self.is_symbol = token not in {".", " "} and not self.is_digit
        self.is_gear = token == "*"

    def __str__(self):
        return str(self.token)

    def __repr__(self):
        return str(self)


class Map(collections.UserDict):
    """
    A map representing a 2D plane made up of tokens.
    """

    def __getitem__(self, item: Position):
        try:
            return super().__getitem__(item)
        except KeyError:
            return Token(" ")

    def __setitem__(self, key: Position, value: Token):
        super().__setitem__(key, value)


@dataclasses.dataclass
class PartNumber:
    """
    A part number in the engine schematic.
    """

    _number: str = ""
    _is_part_number: bool = False
    start_location: Position | None = None
    end_location: Position | None = None

    def __str__(self):
        return str(self._number)

    def __repr__(self):
        return str(self)

    def __add__(self, other: Token):
        self._number += other
        return self

    @property
    def number(self) -> int:
        return int(self._number)

    @property
    def is_part_number(self) -> bool:
        return self._is_part_number

    @is_part_number.setter
    def is_part_number(self, value: bool):
        self._is_part_number = self._is_part_number or value

    def reset(self):
        self._number = ""
        self._is_part_number = False
        self.start_location = None
        self.end_location = None

    def contains(self, position: Position) -> bool:
        """
        Return whether the part number contains the given position.
        """
        assert self.start_location is not None
        assert self.end_location is not None

        # There's a bug somewhere that's causing these to be nested tuples
        start_location = self.start_location[0]
        end_location = self.end_location[0]
        logging.debug(
            f"Checking if {start_location, end_location} contains {position}."
        )

        return start_location <= position <= end_location


class EngineSchematic:
    """
    The engine schematic.
    """

    schematic: Map
    size: tuple[int, int]

    def __init__(self, schematic: Map, size: tuple[int, int]):
        self.schematic = schematic
        self.size = size

    def __str__(self):
        return self.as_str

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for j in range(self.height):
            for i in range(self.width):
                yield Position(j, i)

    @property
    def width(self) -> int:
        return self.size[0] + 1

    @property
    def height(self) -> int:
        return self.size[1] + 1

    @classmethod
    def from_text(cls, text: str) -> EngineSchematic:
        """
        Parse the text document into an engine schematic.
        """
        logging.debug(f"Parsing the following text into an engine schematic:\n{text}")

        schematic = Map()
        for i, line in enumerate(text.strip().splitlines()):
            logging.debug(f"Line {i}: {line}")
            for j, token in enumerate(line):
                logging.debug(f"Token {j}: {token}")
                schematic[Position(i, j)] = Token(token)

        return cls(schematic, (i, j))  # noqa

    @classmethod
    @functools.cache
    def from_file(cls, filename: str) -> EngineSchematic:
        """
        Create an engine schematic from a file.
        """
        file = pathlib.Path(__file__).parent / filename
        logging.info(f"Parsing the following file into an engine schematic: {file}")

        return cls.from_text(file.read_text("utf-8"))

    @functools.cached_property
    def as_str(self) -> str:
        """
        Return the schematic as a string.
        """
        image = ""
        for i, position in enumerate(self):
            token = self.schematic[position]
            image += "\n" if i % self.width == 0 else ""
            image += token.token

        return image

    def _part_numbers(self) -> Generator[PartNumber, None, None]:
        """
        Return the part numbers in the schematic.
        """
        current_number = PartNumber()

        for i, position in enumerate(self):
            token = self.schematic[position]
            end_of_line = i % self.width == self.width - 1

            if token.is_digit:
                neighbours = [self.schematic[pos] for pos in position.neighbours]

                if current_number.start_location is None:
                    logging.debug(f"Found a new part number at {position}.")
                    current_number.start_location = position

                current_number += token.token
                current_number.is_part_number = any(
                    neighbour.is_symbol for neighbour in neighbours
                )

            if end_of_line or not token.is_digit:
                if current_number.is_part_number:
                    current_number.end_location = position + (
                        ZERO if end_of_line else DOWN
                    )  # Confusing, but it works
                    yield copy.deepcopy(current_number)
                current_number.reset()

    @functools.cached_property
    def part_numbers(self) -> list[PartNumber]:
        """
        Return the part numbers in the schematic.
        """
        # Can't cache a generator, so we cache the list instead
        return list(self._part_numbers())

    def gear_ratios(self) -> Generator[int, None, None]:
        """
        Return the gear ratios in the schematic.

        A gear is any * symbol that is adjacent to exactly two part numbers. Its
        gear ratio is the result of multiplying those two numbers together.
        """
        parts = list(self.part_numbers)

        for position in self:
            if not self.schematic[position].is_gear:
                continue

            neighbours = [
                part
                for part in parts
                if any(part.contains(neighbour) for neighbour in position.neighbours)
            ]

            if len(neighbours) != 2:
                continue

            yield neighbours[0].number * neighbours[1].number


def solution(input_: str) -> list[int]:
    """
    Solve the day 3 problem!
    """
    # logging.basicConfig(level="DEBUG")
    logging.basicConfig(level="INFO")

    engine_schematic = EngineSchematic.from_text(input_)

    return [
        sum(part.number for part in engine_schematic.part_numbers),
        sum(engine_schematic.gear_ratios()),
    ]
