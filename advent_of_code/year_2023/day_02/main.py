"""
Solution for day 2.
"""

from __future__ import annotations

import collections
import functools
import logging
import operator
import pathlib
import textwrap
from typing import Literal

BagConfiguration = dict[Literal["red", "green", "blue"], int]


class Cubes(collections.UserDict):
    """
    A set of revealed cubes.
    """

    @classmethod
    def from_text(cls, text: str) -> Cubes:
        """
        Parse the cube count text into a ``Cubes`` object.

        The text is expected to be of the form::

            a blue, b red, c green
        """
        logging.debug(f"Parsing the following text into cubes: {text}")

        class_ = cls()
        cubes = text.split(",")  # ["a blue", "b red", "c green"]
        for cube in cubes:
            cube_count, cube_color = cube.strip().split()
            class_[cube_color] = int(cube_count)

        return class_


class Game:
    """
    A game of cube conundrum.

    Each game has a unique ID and a list of revealed cubes.
    """

    id: int
    revealed_cubes: list[Cubes]

    def __str__(self):
        return str(self.revealed_cubes)

    def __repr__(self):
        return str(self)

    def __init__(self, id_: int, revealed_cubes: list[Cubes]):
        self.id = id_
        self.revealed_cubes = revealed_cubes

    @classmethod
    def from_text(cls, text: str) -> Game:
        """
        Parse the text document into a calibration document object.

        The text document is expected to be of the form::

            Game n: a blue, b red, c green; x blue, y red, z green; ...
        """
        logging.debug(f"Parsing the following text into a cube game: {text}")

        game_id, revealed_cubes = text.strip().split(":")

        return cls(
            id_=int(game_id.split()[1]),
            revealed_cubes=[Cubes.from_text(s) for s in revealed_cubes.split(";")],
        )

    def is_possible(self, bag_configuration: BagConfiguration) -> bool:
        """
        Return True if the game is possible given the bag configuration.
        """
        for cubes in self.revealed_cubes:
            for cube_color, cube_count in cubes.items():
                if cube_count > (bag_count := bag_configuration[cube_color]):
                    logging.debug(
                        textwrap.dedent(
                            f"The game {self.id} is not possible because there are"
                            f" not enough {cube_color} cubes in the bag (there are"
                            f" only {bag_count}, but {cube_count} were revealed)."
                        )
                    )
                    return False
        return True

    def power(self) -> int:
        """
        The power of the game, which is the minimum number of cubes required for
        the game to be possible multiplied together.
        """
        minimal_bad_configuration: BagConfiguration = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }

        for cubes in self.revealed_cubes:
            for cube_color, cube_count in cubes.items():
                minimal_bad_configuration[cube_color] = max(
                    minimal_bad_configuration[cube_color],
                    cube_count,
                )

        return functools.reduce(operator.mul, minimal_bad_configuration.values())


class Games(collections.UserDict):
    """
    A collection of games.
    """

    @classmethod
    def from_text(cls, text: str) -> Games:
        """
        Parse the text document into a ``Games`` object.
        """
        logging.debug(f"Parsing the following text into a game:\n{text}")

        games = [Game.from_text(game) for game in text.strip().splitlines()]

        return cls({game.id: game for game in games})

    @classmethod
    @functools.cache
    def from_file(cls, filename: str) -> Games:
        """
        Parse the file into a``Games`` object.

        The file name is relative to the current module.
        """
        file = pathlib.Path(__file__).parent / filename
        logging.info(f"Parsing the following file into cube games: {file}")

        return cls.from_text(file.read_text("utf-8"))

    def is_possible(self, bag_configuration: BagConfiguration) -> int:
        """
        Sum the IDs for the games that are possible given the bag configuration.
        """
        return sum(
            cube_id
            for cube_id, cube in self.items()
            if cube.is_possible(bag_configuration)
        )

    def power(self) -> int:
        """
        The power of the games, which is the sum of the powers of each game.
        """
        return sum(cube.power() for cube in self.values())


def solution(input_: str) -> list[int]:
    """
    Solve the day 2 problem!
    """
    # logging.basicConfig(level="DEBUG")
    logging.basicConfig(level="INFO")

    bag_configuration: BagConfiguration = {"red": 12, "green": 13, "blue": 14}
    games = Games.from_text(input_)

    return [
        games.is_possible(bag_configuration),
        games.power(),
    ]
