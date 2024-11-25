"""
Solution for day 5.
"""

from __future__ import annotations

import dataclasses
import logging
from typing import Any

ALMANAC_MAPS = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]


def _next_map(map_name: str) -> str:
    """
    Returns the next map name.
    """
    assert map_name in ALMANAC_MAPS

    next_map_prefix = map_name.split("-")[-1]
    for map_ in ALMANAC_MAPS:
        if map_.startswith(next_map_prefix):
            return map_


@dataclasses.dataclass
class MappingParser:
    """
    A mapping, which has a source start, and destination start, and a length.
    """

    destination_start: int
    source_start: int
    length: int

    @property
    def source_end(self) -> int:
        """
        Return the final source index.
        """
        return self.source_start + self.length

    def get_destination(self, source: int) -> int | None:
        """
        Returns the destination for a given source index.
        """
        if self.source_start <= source < self.source_end:
            return self.destination_start + (source - self.source_start)
        else:
            return None


class Map:
    """
    A map, which is a collection of mapping parsers.
    """

    mappings: list[MappingParser]

    def __init__(self, mappings: list[MappingParser]):
        self.mappings = mappings

    def __str__(self):
        return "\n".join(str(mapping) for mapping in self.mappings)

    def __repr__(self):
        return f"Map(mappings={self.mappings})"

    @classmethod
    def from_text(cls, text: str) -> Map:
        """
        Create a map from a text representation.

        For example, the text::

            10 20 3
            30 40 8

        ...would be parsed into two mappings::

            MappingParser(source_start=10, destination_start=20, length=3)
            MappingParser(source_start=30, destination_start=40, length=8)
        """
        logging.debug(f"Parsing map from text:\n{text}")

        mappings = []
        for line in text.strip().splitlines():
            destination_start, source_start, length = line.split()
            mappings.append(
                MappingParser(
                    destination_start=int(destination_start),
                    source_start=int(source_start),
                    length=int(length),
                )
            )

        return cls(mappings)

    def get_destination(self, source: int) -> int:
        """
        Returns the destination for a given source index.

        If no mapping is found, the source index is returned.
        """
        for mapping in self.mappings:
            if (destination := mapping.get_destination(source)) is not None:
                logging.debug(f"Item {source} maps to {destination}")
                return destination

        return source


class Almanac:
    """
    An almanac, which is a collection of maps.
    """

    maps: dict[str, Map]

    def __init__(self, maps: dict[str, Map]):
        self.maps = maps

    def __str__(self):
        return "\n\n".join(
            f"{map_name} map:\n{map_}" for map_name, map_ in self.maps.items()
        )

    def __repr__(self):
        return f"Almanac(maps={self.maps})"

    @classmethod
    def from_text(cls, text: str) -> Almanac:
        """
        Create an almanac from text.
        """
        logging.debug(f"Parsing almanac from text:\n{text}")

        maps = {}
        maps_text = text.split("\n\n")
        for mapping in maps_text:
            map_name, map_text = mapping.split(" map:\n")
            maps[map_name] = Map.from_text(map_text)

        assert set(maps.keys()) == set(ALMANAC_MAPS)

        return cls(maps)

    def get_location(self, seed: int) -> int:
        """
        Returns the location for a given seed.
        """
        logging.debug(30 * "-")
        logging.debug(f"Getting location for seed: {seed}")

        map_name = "seed-to-soil"
        destination = seed
        while True:
            logging.debug(f"Using mapping {map_name}")
            map_ = self.maps[map_name]
            destination = map_.get_destination(destination)
            logging.debug(f"{map_name.split('-')[-1]}: {destination}")
            map_name = _next_map(map_name)
            if map_name is None:
                break

        logging.debug(f"The location for seed {seed} is {destination}")
        return destination


class Seeds:
    """
    A set of seeds.
    """

    _seeds: str

    def __init__(self, _seeds: str):
        self._seeds = _seeds

    def parse_seeds(self, as_range: bool) -> set[int]:
        """
        Create a set of seeds from their text input.
        """
        numbers = self._seeds.split()
        if not as_range:
            return {int(seed) for seed in numbers}

        # If it's a range, the numbers come in pairs. The first number is the
        # starting seed number, and the second number is the number of seeds.
        seeds = []
        while numbers:
            start = int(numbers.pop(0))
            length = int(numbers.pop(0))
            seeds += {start + i for i in range(length)}

        return set(seeds)


def parse_input(text: str) -> tuple[Seeds, Almanac]:
    """
    Parse the input in a set of seeds and an Almanac.
    """
    seeds_text, almanac_text = text.split("\n\n", maxsplit=1)

    if not seeds_text.startswith("seeds: "):
        raise ValueError("Seed text must start with 'seeds: '")

    seeds = Seeds(seeds_text[7:])
    almanac = Almanac.from_text(almanac_text)

    return seeds, almanac


def solution(input_: str) -> list[Any]:
    """
    Solve the day 5 problem!
    """
    logging.basicConfig(level="DEBUG")

    seeds, almanac = parse_input(input_)

    return [
        min(almanac.get_location(seed) for seed in seeds.parse_seeds(as_range=False)),
        min(almanac.get_location(seed) for seed in seeds.parse_seeds(as_range=True)),
    ]
