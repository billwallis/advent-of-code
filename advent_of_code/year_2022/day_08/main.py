"""
OOP solution for day 8.
"""

from __future__ import annotations

import itertools
from typing import Any

from utils.geometry import Position

import advent_of_code.year_2022.day_08.utils as utils


class Tree:
    """
    A tree, which has a height and whether it's visible.
    """

    def __init__(self, height: str | int):
        self.height = int(height)
        self.visible: bool | None = None

    def __str__(self):
        return str(self.height)

    def __repr__(self):
        return f"Tree(height={self.height})"

    def __eq__(self, other: Tree | int):
        return self.height == (other.height if isinstance(other, Tree) else other)

    def __gt__(self, other: Tree | int):
        return self.height > (other.height if isinstance(other, Tree) else other)

    def __ge__(self, other: Tree | int):
        return self > other or self == other

    def __lt__(self, other: Tree | int):
        return not (self >= other)

    def __le__(self, other: Tree | int):
        return self < other or self == other


class Forest:
    """
    A forest, which is a collection of trees at specific positions.
    """

    def __init__(self, trees: str):
        self._trees = trees
        self.forest: list[list[Tree]] = self._get_forest()
        self.shape: tuple[int, int] = (
            len(self.forest),
            max(len(row) for row in self.forest),
        )

    def __str__(self):
        return self._trees

    def __iter__(self):
        yield from self.forest

    def __getitem__(self, position: int | tuple) -> Tree | list:
        """
        Return the item at the specified position.

        The position is row by column, from top to right. For example, the
        positions of a 3 by 3 grid are::

            (0, 0)  (0, 1)  (0, 2)
            (1, 0)  (1, 1)  (1, 2)
            (2, 0)  (2, 1)  (2, 2)
        """
        if isinstance(position, int):
            return utils.chained_get(self.forest, position)
        elif isinstance(position, tuple):
            return utils.chained_get(self.forest, *position)
        else:
            raise ValueError(f"Expected int or tuple, found {type(position)}")

    @property
    def range(self) -> itertools.product:
        # noinspection PyUnresolvedReferences
        """
        Return an iterable-like object for looping through the rows and columns
        in the forest.

        For example, this could be used in the following way (assume a forest
        with 2 rows and 2 columns):

            >>> [print(row, col) for row, col in self.range]
            0 0
            0 1
            1 0
            1 1
        """
        return itertools.product(range(self.shape[0]), range(self.shape[1]))

    @property
    def visibility_matrix(self) -> str:
        """
        Return the visibility matrix for the forest which has the height and
        whether the tree is visible.
        """
        return "\n".join(
            "  ".join([f"({tree.height}, {tree.visible!s:>5})" for tree in row])
            for row in self.forest
        )

    def _get_forest(self) -> list[list[Tree]]:
        """
        Convert the string representation of the trees into a forest.
        """
        return [[Tree(tree) for tree in trees] for trees in self._trees.split("\n")]

    def set_visibility(self) -> None:
        """
        Set whether the trees are visible in the forest.
        """
        for row, col in self.range:
            pos = Position(row, col)
            self[pos].visible = self.is_visible(pos)

    def get_surrounding_trees(self, position: Position) -> list[list[Tree]]:
        """
        For a given position, return a list of 4 lists that contain the trees to
        the left, right, above, and below to the current position (exclusive).
        """
        same_row = self[position[0]]
        same_col = [row[position[1]] for row in self]

        split_row = utils.split_list_at_index(list_=same_row, index_=position[1])
        split_col = utils.split_list_at_index(list_=same_col, index_=position[0])

        return [
            *split_row[:3:2],  # left, right
            *split_col[:3:2],  # up, down
        ]

    def is_edge(self, position: Position) -> bool:
        """
        Return whether the position is on the edge of the forest.
        """
        return position[0] in (0, self.shape[0] - 1) or position[1] in (
            0,
            self.shape[1] - 1,
        )

    def is_visible(self, pos: Position) -> bool:
        """
        Determine whether a tree at a given position is visible in a forest.

        :param pos: The position of the tree.
        :return: ``True`` if the tree is visible, and ``False`` otherwise.
        """
        if self.is_edge(pos):
            # Trees on the edge are always visible
            return True

        # A tree is visible if it can be seen from at least one direction
        tree = self[pos]
        return any(
            tree.height > max(others) for others in self.get_surrounding_trees(pos)
        )

    def compute_scenic_score(self, position: Position) -> int:
        """
        Compute the scenic score of the tree at the given position.

        The scenic score is the product of the count of trees visible in each
        direction from the current position.
        """
        surrounding_trees = self.get_surrounding_trees(position)
        height = self[position].height

        # The surrounding trees are left-to-right and top-to-bottom, so we need
        # to reverse the `left` list and the `up` list
        return (
            utils.directional_score(surrounding_trees[0][::-1], height)  # left
            * utils.directional_score(surrounding_trees[1], height)  # right
            * utils.directional_score(surrounding_trees[2][::-1], height)  # up
            * utils.directional_score(surrounding_trees[3], height)  # down
        )

    def count_visible_trees(self) -> int:
        """
        Return the number of trees that are visible is this forest.
        """
        return sum(int(tree.visible) for row in self for tree in row)

    def find_max_scenic_score(self) -> int:
        """
        Return the number of trees that are visible is this forest.
        """
        return max(
            self.compute_scenic_score(Position(row, col)) for row, col in self.range
        )


def solution(input_: str) -> list[Any]:
    """
    Solve the day 8 problem!
    """
    forest = Forest(input_.strip())
    forest.set_visibility()

    return [
        forest.count_visible_trees(),
        forest.find_max_scenic_score(),
    ]
