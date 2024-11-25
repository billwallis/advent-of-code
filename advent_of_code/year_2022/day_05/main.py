"""
OOP solution for day 5.
"""

from __future__ import annotations

from typing import Any


class Stack(list):
    """
    A stack of items.

    A stack can be represented graphically in the following way::

        [D]
        [C]
        [M]

    This will be stored in a list, such as ``['M', 'C', 'D']``. The order is
    important: the bottom of the stack is on the left of the list (lowest index
    values), and the top of the stack is on the right of the list (highest index
    values).
    """

    def __init__(self, items: list[str]):
        super().__init__(items)

    # def __str__(self):
    #     return "\n".join(f"[{item}]" for item in self)


class Stacks(dict):
    """
    An ordered collection of Stack objects.

    Stacks can be represented graphically in the following way::

            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

    This will be stored in a dictionary where the keys are the stack number (the
    number underneath the stack in the representation above) and the values are
    the Stack objects.
    """

    def __init__(self, stacks: dict[Stack]):
        super().__init__(stacks)

    @classmethod
    def from_graphical_representation(cls, graphical_representation: str) -> Stacks:
        """
        Take the stacks from their graphical representation and convert them
        into dictionaries.

        For example, consider the stacks with the following graphical
        representation::

                [D]
            [N] [C]
            [Z] [M] [P]
             1   2   3

        These will be converted into the following dictionary::

            {
                1: ['Z', 'N'],
                2: ['M', 'C', 'D'],
                3: ['P'],
            }
        """
        row_stacks = [
            [row[(4 * i) + 1 : 4 * (i + 1) - 2] for i in range((len(row) + 1) // 4)]
            for row in graphical_representation.split("\n")
        ]
        items: dict[Stack] = {
            int(col_stacks[0]): Stack(
                items=[
                    col_stacks[i]
                    for i in range(1, len(col_stacks))
                    if col_stacks[i].strip() != ""
                ]
            )
            for col_stacks in zip(*row_stacks[::-1])
        }

        return cls(stacks=items)


class Instruction:
    """
    An instruction to move some number of crates from one stack to another.
    """

    def __init__(self, move_quantity: int, from_stack: int, to_stack: int):
        self.move_quantity = move_quantity
        self.from_stack = from_stack
        self.to_stack = to_stack

    def __str__(self):
        return f"move {self.move_quantity} from {self.from_stack} to {self.to_stack}"

    def __repr__(self):
        return (
            f"Instruction({self.move_quantity=}, {self.from_stack=}, {self.to_stack=})"
        )

    @classmethod
    def from_instruction_text(cls, instruction_text: str) -> Instruction:
        """
        Parse the instruction text into an Instruction object.

        There are several options for the conversion, such as using regex. The
        splitting method has been chosen just for the convenience of the
        implementation.
        """
        tokens = instruction_text.strip().split()
        if tokens[::2] != ["move", "from", "to"]:
            raise ValueError(f"Bad instruction text found: {instruction_text}")

        return cls(
            move_quantity=int(tokens[1]),
            from_stack=int(tokens[3]),
            to_stack=int(tokens[5]),
        )


class Procedure:
    """
    A procedure, which is a set of ordered Instruction objects.
    """

    def __init__(self, procedure: list[Instruction]):
        self.procedure = procedure

    def __str__(self):
        return "\n".join([str(instruction) for instruction in self.procedure])

    def __repr__(self):
        return f"Procedure({self.procedure=})"

    def __iter__(self):
        yield from self.procedure

    @classmethod
    def from_procedure_text(cls, procedure_text: str) -> Procedure:
        """
        Parse the procedure text into a Procedure object.
        """
        return cls(
            [
                Instruction.from_instruction_text(instruction)
                for instruction in procedure_text.strip().split("\n")
            ]
        )


class StackHandler:
    """
    A processor to combine the stacks and procedure.
    """

    def __init__(self, stacks: Stacks, procedure: Procedure):
        self.stacks = stacks
        self.procedure = procedure

    def __str__(self):
        return "\n".join([str(self.stacks), str(self.procedure)])

    def execute_procedure(self, move_multiple_at_once: bool) -> None:
        """
        Execute each of the instructions in the procedure, in order.

        Since the crate mover can move crates both one at a time and multiple at
        a time, we need to know which method should be used to rearrange the
        crates.
        """
        for instruction in self.procedure:
            if move_multiple_at_once:
                crates = [
                    self.stacks[instruction.from_stack].pop()
                    for _ in range(instruction.move_quantity)
                ]
                self.stacks[instruction.to_stack] += crates[::-1]
            else:
                for _ in range(instruction.move_quantity):
                    self.stacks[instruction.to_stack].append(
                        self.stacks[instruction.from_stack].pop()
                    )

    def get_top_of_each_stack(self) -> str:
        """
        Return the top crate from each stack.
        """
        return "".join(stack[-1] for stack in self.stacks.values())


def solution(input_: str) -> list[Any]:
    """
    Solve the day 5 problem!
    """
    _stacks, _procedure = input_.split("\n\n")

    # Need to create the Stacks objects separately otherwise they'll share the
    # same one
    stack_handler_one = StackHandler(
        stacks=Stacks.from_graphical_representation(_stacks),
        procedure=Procedure.from_procedure_text(_procedure),
    )
    stack_handler_many = StackHandler(
        stacks=Stacks.from_graphical_representation(_stacks),
        procedure=Procedure.from_procedure_text(_procedure),
    )

    stack_handler_one.execute_procedure(move_multiple_at_once=False)
    stack_handler_many.execute_procedure(move_multiple_at_once=True)

    return [
        stack_handler_one.get_top_of_each_stack(),
        stack_handler_many.get_top_of_each_stack(),
    ]
