"""
Day 2: Rock, Paper, Scissors!

https://adventofcode.com/2022/day/2
"""

from __future__ import annotations

import enum
import pathlib

from advent_of_code.meta import read_input

PART_1 = 1
PART_2 = 2

ENCODING_OPPONENT = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}
ENCODING_PLAYER_1 = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}
ENCODING_PLAYER_2 = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}

SCORES = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
    "lose": 0,
    "draw": 3,
    "win": 6,
}
# "key defeats value"
DEFEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


class Hand(enum.Enum):
    """
    The played hand, either rock, paper, or scissors.

    This implements **non-transitive** comparisons so that ``hand_1 > hand_2``
    means that ``hand_1`` beats ``hand_2``, but ``hand_1 > hand_2 > hand_3``
    does not imply that ``hand_1 > hand_3``.
    """

    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    def __eq__(self, other: Hand):
        return self.value == other.value

    def __gt__(self, other: Hand):
        return other.value == DEFEATS[self.value]

    def __ge__(self, other: Hand):
        return self > other or self == other

    def __lt__(self, other: Hand):
        return not (self >= other)

    def __le__(self, other: Hand):
        return self < other or self == other

    @classmethod
    def from_opponent_key(cls, opponent_key: str) -> Hand:
        """
        Construct a Hand object from the encoded opponent key.
        """
        return cls(ENCODING_OPPONENT[opponent_key])

    @classmethod
    def from_player_key(cls, player_key: str) -> Hand:
        """
        Construct a Hand object from the encoded player key.
        """
        return cls(ENCODING_PLAYER_1[player_key])


def get_result(opponent: Hand, player: Hand) -> str:
    """
    Determine the player's result of the played hands.

    :param opponent: The opponent's hand.
    :param player: The player's hand.
    :raises ValueError: If the hands can't be compared.
    :return: The player's results. One of ``win``, ``draw``, or ``lose``.
    """
    if player > opponent:
        return "win"
    if player == opponent:
        return "draw"
    if player < opponent:
        return "lose"
    raise ValueError(f"Can't compare hands: {player=}, {opponent=}")


def get_player_hand(opponent: Hand, result: str) -> Hand:
    """
    Determine the player's hand from the result and the opponent's hand.

    :param opponent: The opponent's hand.
    :param result: The player's result. One of `win`, `draw`, or `lose`.
    :return: The player's hand, given the opponent's hand and the result.
    """
    results: dict[str, str] = {
        "win": [
            winner
            for winner, loser in DEFEATS.items()
            if loser == opponent.value
        ][0],
        "draw": opponent.value,
        "lose": DEFEATS[opponent.value],
    }

    return Hand(results[result])


class Round:
    """
    A round of rock, paper, scissors.

    Consists of 2 hands corresponding to the "player" and the "opponent". The
    round has a result and a score for the player.
    """

    def __init__(self, opponent_hand: Hand, player_hand: Hand, result: str):
        self.opponent_hand = opponent_hand
        self.player_hand = player_hand
        self.result = result

    def __repr__(self):
        return f"Round({self.opponent_hand=}, {self.player_hand=}, {self.result=}, {self.score=})"

    @property
    def score(self) -> int:
        """
        The player's score from this round.
        """
        return sum(
            [
                SCORES[self.player_hand.value],
                SCORES[self.result],
            ]
        )

    @classmethod
    def from_part_1(cls, round_input: str) -> Round:
        """
        Construct a round from a round input string.

        The string will consist of two characters. The first corresponds to the
        opponent's hand, and the second corresponds to the player's hand.

        :param round_input: The encoded input for the round.
        :return: A Round object corresponding to the input.
        """
        opponent, player = round_input.split()
        opponent_hand = Hand.from_opponent_key(opponent)
        player_hand = Hand.from_player_key(player)

        return cls(
            opponent_hand=opponent_hand,
            player_hand=player_hand,
            result=get_result(
                opponent=opponent_hand,
                player=player_hand,
            ),
        )

    @classmethod
    def from_part_2(cls, round_input: str) -> Round:
        """
        Construct a round from a round input string.

        The string will consist of two characters. The first corresponds to the
        opponent's hand, and the second corresponds to the player's result.

        :param round_input: The encoded input for the round.
        :return: A Round object corresponding to the input.
        """
        opponent, result = round_input.split()
        opponent_hand = Hand.from_opponent_key(opponent)
        decoded_result = ENCODING_PLAYER_2[result]

        return cls(
            opponent_hand=opponent_hand,
            player_hand=get_player_hand(
                result=decoded_result,
                opponent=opponent_hand,
            ),
            result=decoded_result,
        )


class Strategy:
    """
    The strategy guide.
    """

    def __init__(self, strategy_input: str, part: int):
        """"""
        if part == PART_1:
            self.rounds = [
                Round.from_part_1(round_strategy)
                for round_strategy in strategy_input.split("\n")
            ]
        elif part == PART_2:
            self.rounds = [
                Round.from_part_2(round_strategy)
                for round_strategy in strategy_input.split("\n")
            ]
        else:
            raise ValueError(f"Bad `part` value. Must be 1 or 2, found {part}.")

    def get_total_score(self) -> int:
        """
        Return the sum of the player's scores for each round.
        """
        return sum(rnd.score for rnd in self.rounds)


def solution(use_sample: bool) -> list[int]:
    """
    Solve the day 2 problem!
    """
    file = "sample.data" if use_sample else "input.data"
    input_ = read_input(pathlib.Path(__file__).parent / file)

    strategy_1 = Strategy(input_.strip(), 1)
    strategy_2 = Strategy(input_.strip(), 2)

    return [
        strategy_1.get_total_score(),
        strategy_2.get_total_score(),
    ]
