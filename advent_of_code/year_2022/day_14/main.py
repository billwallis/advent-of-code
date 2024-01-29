"""
OOP solution for day 14.
"""

from __future__ import annotations

import enum
import itertools
from typing import Any

from utils.geometry import Area, Position


class Material(enum.Enum):
    AIR = "."
    ROCK = "#"
    SAND = "o"
    STARTING_SAND = "+"


class Point:
    """
    A point on a map, which has a position and the material that is it filled
    with.
    """

    def __init__(self, position: Position, filled_with: Material):
        self.position = position
        self.filled_with = filled_with

    def __str__(self):
        return f"({self.position[0]}, {self.position[1]}, {self.filled_with})"

    def __repr__(self):
        return f"Point(position={self.position}, filled_with={self.filled_with})"


class Cave:
    def __init__(self):
        self.points: dict[Position, Point] = (
            {}
        )  # Point per coordinate within the dimensions
        self.floor_level = 0
        self._add_starting_sand()

    @property
    def total_area(self) -> Area:
        p_min = Position(
            min(pos[0] for pos in self.points.keys()),
            min(pos[1] for pos in self.points.keys()),
        )
        p_max = Position(
            max(pos[0] for pos in self.points.keys()),
            max(pos[1] for pos in self.points.keys()),
        )

        return Area(p_min, p_max)

    def _add_starting_sand(self) -> None:
        position = START
        self.points[position] = Point(
            position=position, filled_with=Material.STARTING_SAND
        )

    def add_rocks(self, rock_text: str) -> None:
        rock_coordinates = rock_text.split(" -> ")
        for pair in itertools.pairwise(rock_coordinates):
            for position in Area(
                Position.from_text(pair[0]), Position.from_text(pair[1])
            ):
                self.points[position] = Point(
                    position=position, filled_with=Material.ROCK
                )

        self.floor_level = max(pos[1] for pos in self.points.keys()) + 2

    def add_air(self) -> None:
        for position in self.total_area:
            if not self.points.get(position):
                self.points[position] = Point(
                    position=position, filled_with=Material.AIR
                )

    def add_sand(self, position: Position) -> None:
        self.points[position] = Point(position=position, filled_with=Material.SAND)

    def material_at(self, position: Position) -> Material:
        if position[1] >= self.floor_level:
            return Material.ROCK
        elif point := self.points.get(position):
            return point.filled_with
        else:
            return Material.AIR

    def draw(self) -> None:
        image = ""
        air = Point(position=None, filled_with=Material.AIR)  # noqa
        last_position = Position(0, 0)

        for position in self.total_area:
            if position[1] != last_position[1]:
                image += "\n"
            image += self.points.get(position, air).filled_with.value
            last_position = position

        print(image)
        print()


class SandCycle:
    def __init__(self, cave: Cave):
        self.cave = cave
        self.path: list[Position] = []
        self.keep_cycling = True

    @classmethod
    def from_text(cls, text: str) -> SandCycle:
        cave = Cave()
        for formation in text.split("\n"):
            cave.add_rocks(formation)
        cave.add_air()

        return cls(cave)

    def move_sand_until_out_of_range(self) -> None:
        position = self.path[-1]
        while True:
            if self.cave.material_at(position + DOWN) == Material.AIR:
                position += DOWN
            elif self.cave.material_at(position + DOWN + LEFT) == Material.AIR:
                position += DOWN + LEFT
            elif self.cave.material_at(position + DOWN + RIGHT) == Material.AIR:
                position += DOWN + RIGHT
            else:
                self.cave.add_sand(position)
                self.path.pop()
                return

            self.path.append(position)

            if position not in self.cave.total_area:
                self.keep_cycling = False
                self.path.pop()
                return

    def watch_sand_fall_until_out_of_range(self) -> int:
        self.path.append(START)
        while self.keep_cycling:
            self.move_sand_until_out_of_range()
            # self.cave.draw()
            # time.sleep(0.5)

        return len(
            [
                point
                for point in self.cave.points.values()
                if point.filled_with == Material.SAND
            ]
        )

    def move_sand_until_hit_starting_point(self) -> None:
        position = self.path[-1]
        while True:
            if self.cave.material_at(position + DOWN) == Material.AIR:
                position += DOWN
            elif self.cave.material_at(position + DOWN + LEFT) == Material.AIR:
                position += DOWN + LEFT
            elif self.cave.material_at(position + DOWN + RIGHT) == Material.AIR:
                position += DOWN + RIGHT
            elif position == START:
                self.cave.add_sand(position)
                self.path.pop()
                self.keep_cycling = False
                return
            else:
                self.cave.add_sand(position)
                self.path.pop()
                return

            self.path.append(position)

    def watch_sand_fall_until_hit_starting_point(self) -> int:
        self.path.append(START)
        while self.keep_cycling:
            self.move_sand_until_hit_starting_point()
            # self.cave.draw()
            # time.sleep(0.5)

        return len(
            [
                point
                for point in self.cave.points.values()
                if point.filled_with == Material.SAND
            ]
        )


# noinspection DuplicatedCode
UP = Position(0, -1)
DOWN = Position(0, 1)
LEFT = Position(-1, 0)
RIGHT = Position(1, 0)

START = Position(500, 0)


def solution(input_: str) -> list[Any]:
    """
    Solve the day 14 problem!
    """
    sand_cycles_1 = SandCycle.from_text(input_.strip())
    sand_cycles_2 = SandCycle.from_text(input_.strip())

    return [
        sand_cycles_1.watch_sand_fall_until_out_of_range(),
        sand_cycles_2.watch_sand_fall_until_hit_starting_point(),
    ]
