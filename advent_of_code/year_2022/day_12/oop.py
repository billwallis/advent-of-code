"""
OOP solution for day 12.
"""
from __future__ import annotations

import re
import time
from typing import Any

import utils.geometry


class Position(utils.geometry.Position):
    """
    A position on a 2-dimensional plane of integers.
    """

    @property
    def neighbours(self) -> list[Position]:
        """
        Return the positions of the 4 immediate neighbours of the current
        position.
        """
        return [self + direction for direction in [UP, DOWN, LEFT, RIGHT]]


# noinspection DuplicatedCode
# Math co-ordinates
UP = Position(0, 1)
DOWN = Position(0, -1)
LEFT = Position(-1, 0)
RIGHT = Position(1, 0)


class Height:
    """
    A height, determined by a character from ``a`` to ``z``.
    """

    _START_END = {
        "S": "`",  # ` comes before a
        "E": "{",  # { comes after z
    }

    def __init__(self, height: str):
        if not re.match(r"^[a-zSE]$", height):
            raise ValueError(f"Characters between `a` and `z` only, found {height}")
        self.height = height

    def __str__(self):
        return f"'{self.height}'"

    def __repr__(self):
        # return f"Height(height='{self.height}')"
        return f"'{self.height}'"

    def __eq__(self, other: Height):
        return self._height == other._height

    def __gt__(self, other: Height):
        return self._height > other._height

    def __ge__(self, other: Height):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other: Height):
        return not self.__ge__(other)

    def __le__(self, other: Height):
        return not self.__gt__(other)

    def __sub__(self, other: Height):
        return ord(self._height) - ord(other._height)

    def __rsub__(self, other: Height):
        return self.__sub__(other)

    @property
    def _height(self) -> str:
        """
        Return the height used for comparison. This is specific for the case
        where the height are the special cases 'S' and 'E'.
        """
        return self._START_END.get(self.height, self.height)


class Point:
    """
    A point on a map, which has a position, a height, and whether it has been
    visited.
    """

    def __init__(self, position: Position, height: Height):
        self.position = position
        self.height = height
        self.visited = False

    def __str__(self):
        return f"({self.position[0]}, {self.position[1]}, {self.height})"

    def __repr__(self):
        return f"Point(position={self.position}, height={self.height})"


class Hill:
    """
    A hill, which is a plane of 2-dimensional points with a corresponding height
    value.
    """

    def __init__(
        self, map_: dict[Position, Point], starting_point: Point, ending_letter: str
    ):
        """
        Create a hill which is a grid of points, with a start point and end
        point of the route to be found.
        """
        self.map_ = map_
        self.starting_point = starting_point
        self.routes: dict[int, list[Point]] = {
            # Step number: points at step
            0: [starting_point]
        }
        self.starting_point.visited = True
        self.ending_letter = ending_letter
        self.direction = 1 if ending_letter == "E" else -1

    def __str__(self):
        return str(self.map_)

    @classmethod
    def from_text(cls, text: str, starting_letter: str, ending_letter: str) -> Hill:
        """
        Parse a text representation of a map into a Hill.
        """
        points = {}
        for y, row in enumerate(text.split("\n")):
            for x, z in enumerate(row):
                pos = Position(x, -y)
                point = Point(pos, Height(z))
                points[pos] = point
                if z == starting_letter:
                    starting_point = point

        return cls(points, starting_point, ending_letter)  # noqa

    def print_visits(self, current_step: int = None) -> None:
        """
        Print the visitation of the points.
        """
        # Assumes that the positions are already in order
        image = ""
        characters = {
            True: "#",
            False: ".",
        }
        for position, point in self.map_.items():
            if position[0] == 0:
                image += "\n"

            new_visit = point in self.routes[current_step]
            character = "\033[92m@\033[0m" if new_visit else characters[point.visited]
            image += character

        print(image)
        time.sleep(1)

    def can_climb(self, current_height: Height, neighbour_height: Height) -> bool:
        """
        Whether a neighbouring point can be climbed on.
        """
        return self.direction * (neighbour_height - current_height) <= 1

    def find_route(self, print_image: bool = False) -> None:
        """
        Find the shortest route to the exit.
        """
        end = Height(self.ending_letter)
        end_found = False
        step = 0

        while not end_found:
            if print_image:
                self.print_visits(step)

            self.routes[step + 1] = []
            for point in self.routes[step]:
                for neighbour_position in point.position.neighbours:
                    if neighbour := self.map_.get(neighbour_position):
                        if (
                            self.can_climb(
                                current_height=self.map_.get(point.position).height,
                                neighbour_height=neighbour.height,
                            )
                            and not neighbour.visited
                        ):
                            self.routes[step + 1].append(neighbour)
                            neighbour.visited = True
                            if end_found := (neighbour.height == end):
                                return  # Hack to quit, not sure why the while loop doesn't exit

            step += 1


def solution(input_: str) -> list[Any]:
    """
    Solve the day 12 problem!
    """
    hill_1 = Hill.from_text(input_.strip(), starting_letter="S", ending_letter="E")
    hill_1.find_route(print_image=False)
    hill_2 = Hill.from_text(input_.strip(), starting_letter="E", ending_letter="a")
    hill_2.find_route(print_image=False)

    return [
        max(hill_1.routes.keys()),
        max(hill_2.routes.keys()),
    ]
