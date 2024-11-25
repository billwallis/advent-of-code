"""
OOP solution for day 17.
"""

from __future__ import annotations

import abc
import copy
from typing import Any

from utils.geometry import Position


class COLOURS:
    """
    Taken from:

    - https://stackoverflow.com/a/287944/8213085
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# noinspection DuplicatedCode
# Math co-ordinates
ZERO = Position(0, 0)
UP = Position(0, 1)
DOWN = Position(0, -1)
LEFT = Position(-1, 0)
RIGHT = Position(1, 0)


class Rock(abc.ABC):
    height: int = 0
    width: int = 0
    _shape: list[Position] = []

    def __init__(self, top_left: Position):
        self.top_left = top_left  # x (left), y (top)

    def __str__(self):
        return f"{self.__class__.__name__} at {self.top_left}"

    @property
    def shape(self) -> set[Position]:
        return {self.top_left + position for position in self._shape}

    @property
    def right_boundary(self) -> int:
        return self.top_left[0] + self.width - 1

    @property
    def bottom_boundary(self) -> int:
        return self.top_left[1] + self.height - 1

    def move(self, direction: Position) -> None:
        self.top_left += direction

    def draw(self) -> None:
        image = ""
        for y in range(self.height):
            image += "\n"
            for x in range(self.width):
                image += "#" if Position(x, -y) in self._shape else "."

        print(image)


class Horizontal(Rock):
    height: int = 1
    width: int = 4
    _shape: list[Position] = [
        Position(0, 0),
        Position(0, 0) + RIGHT,
        Position(0, 0) + (RIGHT * 2),
        Position(0, 0) + (RIGHT * 3),
    ]

    def __init__(self, top_left: Position):
        super().__init__(top_left=top_left)


class Plus(Rock):
    height: int = 3
    width: int = 3
    _shape: list[Position] = [
        Position(0, 0) + RIGHT,
        Position(0, 0) + DOWN,
        Position(0, 0) + RIGHT + DOWN,
        Position(0, 0) + (RIGHT * 2) + DOWN,
        Position(0, 0) + RIGHT + (DOWN * 2),
    ]

    def __init__(self, top_left: Position):
        super().__init__(top_left=top_left)


class Bend(Rock):
    height: int = 3
    width: int = 3
    _shape: list[Position] = [
        Position(0, 0) + (RIGHT * 2),
        Position(0, 0) + (RIGHT * 2) + DOWN,
        Position(0, 0) + (RIGHT * 2) + (DOWN * 2),
        Position(0, 0) + RIGHT + (DOWN * 2),
        Position(0, 0) + (DOWN * 2),
    ]

    def __init__(self, top_left: Position):
        super().__init__(top_left=top_left)


class Vertical(Rock):
    height: int = 4
    width: int = 1
    _shape: list[Position] = [
        Position(0, 0),
        Position(0, 0) + DOWN,
        Position(0, 0) + (DOWN * 2),
        Position(0, 0) + (DOWN * 3),
    ]

    def __init__(self, top_left: Position):
        super().__init__(top_left=top_left)


class Square(Rock):
    height: int = 2
    width: int = 2
    _shape: list[Position] = [
        Position(0, 0),
        Position(0, 0) + RIGHT,
        Position(0, 0) + DOWN,
        Position(0, 0) + RIGHT + DOWN,
    ]

    def __init__(self, top_left: Position):
        super().__init__(top_left=top_left)


def intersection(shape_1: Rock, shape_2: Rock) -> bool:
    return shape_1.shape.intersection(shape_2.shape) != {}


class Jets:
    DIRECTION: dict[str, Position] = {
        "<": LEFT,
        ">": RIGHT,
    }

    def __init__(self, jet_text: str):
        self.jets = jet_text
        self._current_jet = 0

    def get(self) -> Position:
        jet = self.jets[self._current_jet]
        self._current_jet = (self._current_jet + 1) % len(self.jets)

        return self.DIRECTION[jet]


class Chamber:
    def __init__(self, width: int, jet_text: str):
        self.width = width  # Positions from 1 to width, inclusive
        self.jets = Jets(jet_text)
        self.contents: dict[Position, str] = {}  # Position, type of rock
        self.rocks: list[Rock] = []
        self.rock_cycle = 0
        self.top_height = 0

        self.add_floor()

    def add_floor(self) -> None:
        """
        Create the floor of the chamber.
        """
        for i in range(1, 1 + self.width):
            self.contents[Position(i, 0)] = "F"

    def add_rock(self, from_left: int = 2, from_bottom: int = 3) -> Rock:
        """
        Add a new rock to the chamber.

        New rocks appears so that its left edge is two units away from the left
        wall and its bottom edge is three units above the highest rock in the
        room.
        """
        new_rock_cls = ROCK_ORDER[self.rock_cycle]
        self.rock_cycle = (self.rock_cycle + 1) % 5

        new_rock = new_rock_cls(
            top_left=Position(
                from_left + 1,
                from_bottom + self.top_height + new_rock_cls.height,
            )
        )
        self.rocks.append(new_rock)

        return new_rock

    def is_conflict(self, rock: Rock, direction: Position) -> bool:
        """
        Check whether moving a rock by a direction results in a conflict.
        """
        moved_rock = copy.copy(rock)
        moved_rock.move(direction)

        return any(position in self.contents.keys() for position in moved_rock.shape)

    def jet_movement(self, rock: Rock) -> Position:
        """
        Determine how to move the rock by the jet.
        """
        jet = self.jets.get()
        if self.is_conflict(rock, jet):
            return ZERO
        elif jet == LEFT:
            return ZERO if rock.top_left[0] <= 1 else LEFT
        elif jet == RIGHT:
            return ZERO if rock.right_boundary >= (self.width - 1) else RIGHT

    def move_rock(self, rock: Rock) -> None:
        """
        Move the rock through the chamber.

        A move consists of a push by the jet (if possible), followed by moving
        down until it lands on another rock (or the floor).
        """
        while True:
            rock.move(direction=self.jet_movement(rock=rock))

            if not self.is_conflict(rock, DOWN):
                rock.move(direction=DOWN)
            else:
                # Save the current position
                for position in rock.shape:
                    self.contents[position] = rock.__class__.__name__[0]
                # Set the new height
                self.top_height = max(self.top_height, rock.top_left[1])
                return

    def run(self, rock_limit: int, draw: bool = False) -> None:
        """
        Continue adding and moving rocks until the limit.
        """
        while len(self.rocks) < rock_limit:
            new_rock = self.add_rock()
            self.move_rock(new_rock)

            if draw:
                self.draw()

    def _draw(self) -> None:
        image = ""
        for y in range(self.top_height + 1):
            image += "\n"
            for x in range(1, 1 + self.width):
                y_ = self.top_height - y
                image += (
                    "@"
                    if y_ == 0
                    else "#" if Position(x, y_) in self.contents.keys() else "."
                )

        print(image)

    def draw(self) -> None:
        icons = {
            ".": ".",
            "F": f"{COLOURS.HEADER}@{COLOURS.ENDC}",
            "H": f"{COLOURS.OKBLUE}#{COLOURS.ENDC}",
            "P": f"{COLOURS.OKCYAN}#{COLOURS.ENDC}",
            "B": f"{COLOURS.OKGREEN}#{COLOURS.ENDC}",
            "V": f"{COLOURS.WARNING}#{COLOURS.ENDC}",
            "S": f"{COLOURS.FAIL}#{COLOURS.ENDC}",
        }
        image = ""
        for y in range(self.top_height + 1):
            image += "\n"
            for x in range(1, 1 + self.width):
                y_ = self.top_height - y
                image += icons.get(self.contents.get(Position(x, y_), "."))

        print(image)


ROCK_ORDER: dict[int, type[Rock]] = {
    0: Horizontal,
    1: Plus,
    2: Bend,
    3: Vertical,
    4: Square,
}


def solution(input_: str) -> list[Any]:
    """
    Solve the day 17 problem!
    """
    chamber = Chamber(width=7, jet_text=input_.strip())
    chamber.run(rock_limit=2022, draw=False)
    # chamber.draw()

    return [
        chamber.top_height,
        0,
    ]
