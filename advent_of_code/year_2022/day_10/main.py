"""
OOP solution for day 10.
"""

from typing import Any


class Scheduler(dict):
    """
    The history of scheduled events.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: int, value: int):
        """
        Append an item to the values of a key.

        Setting an item in a scheduler that already exists just appends the new
        items. This is because many event may need to be run on a particular
        cycle.
        """
        value = self.get(key, []) + [value]
        super().__setitem__(key, value)

    def add_event(self, at: int, value: int) -> None:
        """
        Add a scheduled event for a value at a particular time.
        """
        self[at] = value


# sourcery skip: upper-camel-case-classes
class CRT:
    """
    The CRT, which draws a sprite on some pixels.
    """

    def __init__(self, starting_position: int):
        self.position = starting_position
        self.drawing = ""

    @property
    def sprite(self) -> list[int]:
        """
        The pixels that the sprite currently occupy.
        """
        return [self.position + i for i in range(3)]

    def add_pixel(self, is_lit: bool) -> None:
        """
        Draw a pixel on the drawing, which may be lit.
        """
        self.drawing += "#" if is_lit else "."


class CPU:
    """
    The CPU, which has a register and can take instructions.
    """

    def __init__(self):
        self.cycle = 0
        self.registries = {}
        self.scheduler = Scheduler()
        self.interesting_signals = {}
        self.crt: CRT | None = None

    def add_registry(self, registry: str, starting_value: int = 1) -> None:
        """
        Add a registry to the CPU.
        """
        self.registries[registry] = starting_value
        self.crt = CRT(starting_value)

    def set_registry(self, registry: str, value: int) -> None:
        """
        Set the value of a registry.
        """
        self.registries[registry] = value

    def get_registry(self, registry: str) -> int:
        """
        Get the value of a registry.
        """
        return self.registries[registry]

    def parse_instruction(self, instruction: str) -> int:
        """
        Parse the instructions, returning the cycle time taken to complete.
        """
        if instruction == "noop":
            return 1
        elif instruction.startswith("addx"):
            vals = instruction.split()
            self.scheduler.add_event(at=self.cycle + 2, value=int(vals[1]))
            return 2

    def resolve_schedule(self) -> None:
        """
        Update the value of the registry using the scheduled events.
        """
        self.registries["X"] += sum(self.scheduler.get(self.cycle, [0]))
        self.crt.position = self.registries["X"]

    def execute(self, instructions: list[str], interesting_signals: list[int]) -> None:
        """
        Execute a set of instructions.
        """
        for instruction in instructions:
            execution_time = self.parse_instruction(instruction)
            for _ in range(execution_time):
                self.cycle += 1

                if self.cycle in interesting_signals:
                    self.interesting_signals[self.cycle] = self.registries["X"]

                self.crt.add_pixel((self.cycle % 40) in self.crt.sprite)

                self.resolve_schedule()

    def print_drawing(self) -> str:
        """
        Print the drawing of the CRT.
        """
        length = len(self.crt.drawing)
        drawing = "\n".join(
            [self.crt.drawing[40 * i : 40 * (i + 1)] for i in range(length // 40)]
        )

        print(drawing)
        return drawing


def solution(input_: str) -> list[Any]:
    """
    Solve the day 10 problem!
    """
    cpu = CPU()
    cpu.add_registry(registry="X", starting_value=1)
    cpu.execute(
        instructions=input_.strip().split("\n"),
        interesting_signals=[20, 60, 100, 140, 180, 220],
    )
    final_drawing = cpu.print_drawing()
    print()

    return [
        sum(cycle * strength for cycle, strength in cpu.interesting_signals.items()),
        final_drawing,
    ]
