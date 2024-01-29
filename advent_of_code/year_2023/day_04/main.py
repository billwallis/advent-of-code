"""
Solution for day 4.
"""

from __future__ import annotations

import collections
import functools
import logging


class Scratchcard:
    """
    A scratchcard, which has some winning numbers and some numbers we have.
    """

    card_id: int
    winning_numbers: list[int]
    held_numbers: list[int]

    def __init__(
        self,
        card_id: int,
        winning_numbers: list[int],
        held_numbers: list[int],
    ) -> None:
        self.card_id = card_id
        self.winning_numbers = winning_numbers
        self.held_numbers = held_numbers

    def __str__(self):
        return self.as_str

    def __repr__(self):
        return str(self)

    @functools.cached_property
    def as_str(self) -> str:
        """
        Return the scratchcard as a string.
        """
        winning_numbers = " ".join([f"{number:>2}" for number in self.winning_numbers])
        held_numbers = " ".join([f"{number:>2}" for number in self.held_numbers])

        return f"Card {self.card_id}: {winning_numbers} | {held_numbers}"

    @classmethod
    def from_text(cls, text: str) -> Scratchcard:
        """
        Parse the text document into a scratchcard.

        The text document is expected to be of the form::

            Card n: a b c | x y z
        """
        logging.debug(f"Parsing the following text into a scratchcard: {text}")

        card_id, numbers = text.strip().split(":")
        winning_numbers, held_numbers = numbers.strip().split("|")

        return cls(
            card_id=int(card_id.split()[1]),
            winning_numbers=[int(number) for number in winning_numbers.strip().split()],
            held_numbers=[int(number) for number in held_numbers.strip().split()],
        )

    @functools.cached_property
    def matches(self) -> set[int]:
        """
        Return the numbers that match.
        """
        matches = set(self.winning_numbers).intersection(set(self.held_numbers))
        logging.debug(f"Matches in card {self.card_id}: {matches}")

        return matches

    def total_points(self) -> int:
        """
        Calculate the total points for this scratchcard.

        The first match makes the card worth one point and each match after the
        first doubles the point value of that card.
        """
        return 2 ** (len(self.matches) - 1) if self.matches else 0


class ScratchcardCounter(collections.UserDict):
    """
    Track and count the number of scratchcards in the game.
    """

    def __init__(self, scratchcards: list[Scratchcard]) -> None:
        super().__init__()
        self._scratchcards = scratchcards
        for i in range(1, 1 + len(scratchcards)):
            self[i] = 1

    def play(self) -> None:
        """
        Play the scratchcards.
        """
        for scratchcard in self._scratchcards:
            copies = self[scratchcard.card_id]
            logging.debug(
                f"Playing card {scratchcard.card_id} which has {copies} copies."
            )
            logging.debug(
                f"Card {scratchcard.card_id} has {len(scratchcard.matches)} matches."
            )
            for i in range(1, 1 + len(scratchcard.matches)):
                self[scratchcard.card_id + i] += copies


def solution(input_: str) -> list[int]:
    """
    Solve the day 4 problem!
    """
    logging.basicConfig(level="INFO")

    scratchcards = [Scratchcard.from_text(line) for line in input_.splitlines()]
    scratchcard_counter = ScratchcardCounter(scratchcards)
    scratchcard_counter.play()

    return [
        sum(card.total_points() for card in scratchcards),
        sum(scratchcard_counter.values()),
    ]
