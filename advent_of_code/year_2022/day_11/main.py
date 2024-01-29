"""
OOP solution for day 11.
"""

from __future__ import annotations

import math
from typing import Any


class Item:
    """
    An item, which just has a worry level.
    """

    def __init__(self, worry_level: int):
        self._worry_level = worry_level
        self.worry_history = [worry_level]

    def __str__(self):
        return str(self.worry_level)

    def __repr__(self):
        return f"Item(worry_level={self.worry_level})"

    @property
    def worry_level(self) -> int:
        return self._worry_level

    @worry_level.setter
    def worry_level(self, value: int):
        self._worry_level = value
        self.worry_history.append(value)


class Monkey:
    """
    A Monkey, which hold items, inspects items, and throws items.
    """

    def __init__(
        self,
        monkey_id: int,
        items: list[Item],
        operation: str,
        test: str,
        test_outcome: dict[bool, int],
    ):
        """
        Create a Monkey object.

        :param items: A list of integers corresponding to the items
         that the monkey starts with.
        :param operation: A operation that the monkey performs. Must be a string
         something like `new = old * 19`.
        :param test: A test that the monkey performs. Must be a string something
         like `divisible by 23`.
        """
        self.id = monkey_id
        self.items = items
        self._operation = operation
        self._test = test
        self._outcome = test_outcome
        self.inspection_count: int = 0
        self.divisor = int(self._test.split()[2])

    def __repr__(self):
        return (
            f"Monkey("
            f"monkey_id={self.id}, "
            f"items={self.items}, "
            f"operation='{self._operation}', "
            f"test='{self._test}', "
            f"test_outcome={self._outcome}"
            f")"
        )

    @classmethod
    def from_string_block(cls, text: str) -> Monkey:
        """
        Convert a block of text into a Monkey.

        The text is expected to be of the following format::

            Monkey 0:
              Starting items: 79, 98
              Operation: new = old * 19
              Test: divisible by 23
                If true: throw to monkey 2
                If false: throw to monkey 3
        """
        lines = [line.strip() for line in text.strip().split("\n")]

        monkey_id = int(lines[0][:-1].replace("Monkey ", ""))
        items = eval(f"[{lines[1].replace('Starting items: ', '')}]")
        starting_items = [Item(item) for item in items]
        operation = lines[2].replace("Operation: ", "")
        test = lines[3].replace("Test: ", "")
        test_outcome = {
            True: int(lines[4].replace("If true: throw to monkey ", "")),
            False: int(lines[5].replace("If false: throw to monkey ", "")),
        }

        return cls(
            monkey_id=monkey_id,
            items=starting_items,
            operation=operation,
            test=test,
            test_outcome=test_outcome,
        )

    def evaluate_worry(self, old: int) -> int:
        """
        Evaluate the operation.
        """
        assert "old" in self._operation
        return eval(self._operation.replace("new = ", ""))

    def test(self, num: int) -> bool:
        """
        Test the input using the monkey's logic.
        """
        components = self._test.split()
        if components[0] == "divisible":
            return (num % int(components[2])) == 0
        else:
            raise NotImplementedError(
                f"Monkey.test() not implemented for test {self._test}"
            )

    def throw_to(self, item: Item) -> int:
        """
        Determine which monkey the current monkey will throw the item to.
        """
        return self._outcome[self.test(item.worry_level)]

    def inspect_item(
        self, item: Item, worry_divisor: int, total_divisor: int = None
    ) -> None:
        """
        Inspect an item that the monkey is holding.
        """
        assert item in self.items
        self.inspection_count += 1

        # Taking the remainder from total_divisor doesn't impact the divisibility
        # of the values, but stops them from growing so large that the program
        # slows to a halt
        item.worry_level = (
            self.evaluate_worry(item.worry_level) // worry_divisor
        ) % total_divisor


class Rounds:
    """
    Round handler for monkeys inspecting items and throwing them to each other.
    """

    def __init__(self, monkeys: dict[int, Monkey], worry_divisor: int):
        self.monkeys = monkeys
        self.worry_divisor = worry_divisor
        self.total_divisor = math.prod([monkey.divisor for monkey in monkeys.values()])

    def move_item(self, item: Item, from_id: int, to_id: int) -> None:
        """
        Move an item from one monkey to another.
        """
        self.monkeys[from_id].items.remove(item)
        self.monkeys[to_id].items.append(item)

    def _run_round(self) -> None:
        """
        Run a round of monkeys inspecting items and throwing them to each other.
        """
        for monkey_id, monkey in self.monkeys.items():
            while monkey.items:
                item = monkey.items[0]
                monkey.inspect_item(item, self.worry_divisor, self.total_divisor)
                self.move_item(
                    item=item,
                    from_id=monkey_id,
                    to_id=monkey.throw_to(item),
                )

    def run_rounds(self, rounds: int) -> None:
        """
        Run a number of rounds of monkeys inspecting items and throwing them to
        each other.
        """
        for i in range(rounds):
            self._run_round()
            if (i + 1) % 1_000 == 0:
                self.print_inspection_counts(i + 1)

    def print_inspection_counts(self, round_number: int) -> None:
        """
        Print the inspection counts for each of the monkeys.
        """
        print(f"== After round {round_number} ==")
        for monkey_id, monkey in self.monkeys.items():
            print(f"Monkey {monkey_id} inspected items {monkey.inspection_count} times")

    @property
    def monkey_business(self) -> int:
        """
        Determine the current level of monkey business, which is the product of
        the top 2 counts of inspections.
        """
        inspection_counts = sorted(
            [monkey.inspection_count for monkey in self.monkeys.values()]
        )
        return math.prod(inspection_counts[-2:])


def make_monkeys(input_: str) -> dict[int, Monkey]:
    """
    Convert the input string into a collection of monkeys.
    """
    return {
        monkey.id: monkey
        for monkey in [Monkey.from_string_block(line) for line in input_.split("\n\n")]
    }


def solution(input_: str) -> list[Any]:
    """
    Solve the day 11 problem!
    """
    rounds_1 = Rounds(make_monkeys(input_), 3)
    rounds_1.run_rounds(20)
    rounds_2 = Rounds(make_monkeys(input_), 1)
    rounds_2.run_rounds(10_000)

    return [
        rounds_1.monkey_business,
        rounds_2.monkey_business,
    ]
