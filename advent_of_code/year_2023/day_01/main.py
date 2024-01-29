"""
Solution for day 1.
"""

from __future__ import annotations

import functools
import logging
import pathlib
from typing import Callable

Procedure = Callable[[str], int]

DIGITS = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


class CalibrationDocument:
    """
    A calibration document.

    This is a document with a list of lines. Each line contains some text
    with some numbers amongst some text.
    """

    lines: list[str]

    def __init__(self, lines: list[str]):
        self.lines = lines

    @classmethod
    def from_text(cls, text: str) -> CalibrationDocument:
        """
        Parse the text document into a calibration document object.
        """
        logging.debug(
            f"Parsing the following text into a calibration document:\n{text}"
        )

        return cls(text.strip().splitlines())

    @classmethod
    @functools.cache
    def from_file(cls, filename: str) -> CalibrationDocument:
        """
        Parse the file into a calibration document object.

        The file name is relative to the current module.
        """
        file = pathlib.Path(__file__).parent / filename
        logging.info(f"Parsing the following file into a calibration document: {file}")

        return cls.from_text(file.read_text("utf-8"))

    def process_lines(self, procedure: Procedure) -> int:
        """
        Execute the procedure on the lines and return the sum of their
        results.
        """
        return sum(procedure(line) for line in self.lines)


def first_and_last_digit(line: str) -> int:
    """
    Concatenate and return the first and last digits of the line.

    If the line only has a single digit, it will be used as both the first
    and the last digit.

    If the line has no digits, 0 will be used as both the first and the last
    digit instead.
    """
    digits = [c for c in line if c.isdigit()] or ["0"]
    logging.debug(f"The text {line} has the digits {digits}")

    return int("".join([digits[0], digits[-1]]))


def _get_digit(line: str, digits: list[str]) -> str | None:
    """
    Return the digit at the start of the line if one exists, else return
    ``None``.
    """
    for digit in digits:
        logging.debug(f"Searching {line[: len(digit)]} for {digit}")
        if (token := line[: len(digit)]) == digit:
            return token


def first_and_last_number(text: str) -> int:
    """
    Concatenate and return the first and last numbers of the line.

    Note that a "number" is any digit expressed as a number or as a word.
    For example, both ``1`` and ``one`` would be considered numbers.

    If the line only has a single number, it will be used as both the first
    and the last digit.
    """
    first_number, last_number = None, None

    for i in range(len(text)):
        if first_number := _get_digit(text[i:], list(DIGITS)):
            break

    rev_text = text[::-1]
    for i in range(len(rev_text)):
        if last_number := _get_digit(rev_text[i:], [d[::-1] for d in list(DIGITS)]):
            last_number = last_number[::-1]
            break

    logging.debug(f"The text {text} has the digits {[first_number, last_number]}")
    return int("".join([DIGITS[first_number], DIGITS[last_number]]))


def solution(input_: str) -> list[int]:
    """
    Solve the day 1 problem!
    """
    # logging.basicConfig(level="DEBUG")
    logging.basicConfig(level="INFO")

    calibration_document = CalibrationDocument.from_text(input_)

    return [
        calibration_document.process_lines(first_and_last_digit),
        calibration_document.process_lines(first_and_last_number),
    ]
