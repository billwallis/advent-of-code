"""
OOP solution for day 16.
"""
from __future__ import annotations

import copy
import re
from typing import Any


class Valve:
    def __init__(self, name: str, flow_rate: int):
        self.name = name
        self.flow_rate = flow_rate
        self.leads_to: list[Valve] = []
        self.open = False

    def __str__(self):
        return f"<'{self.name}': {self.flow_rate} {self.open_icon}>"

    def __repr__(self):
        return self.__str__()

    @property
    def open_icon(self) -> str:
        return {True: "◉", False: "○"}[self.open]


class Valves:
    def __init__(self, valves: list[Valve], tunnels: dict[str, list[str]]):
        self.valves = valves
        self.tunnels = tunnels

        for valve in self.valves:
            valve.leads_to = [self[v] for v in self.tunnels[valve.name]]

    def __str__(self):
        return "[" + ", ".join(str(valve) for valve in self) + "]"

    def __iter__(self):
        yield from self.valves

    def __getitem__(self, item: str) -> Valve:
        for valve in self.valves:
            if valve.name == item:
                return valve

    @classmethod
    def from_text(cls, text: str) -> Valves:
        items = [
            re.sub(
                r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)$",
                repl=r"\1,\2,\3",
                string=line,
            ).split(",", 2)
            for line in text.split("\n")
        ]

        valves = [Valve(item[0], int(item[1])) for item in items]
        tunnels = {item[0]: item[2].split(", ") for item in items}

        return cls(valves=valves, tunnels=tunnels)


class Route:
    def __init__(self, input_: str):
        self.valves = Valves.from_text(input_)
        self._current_valve = "AA"
        self.current_pressure = 0
        self.open_valves = []
        self.id = "1"

    def __str__(self):
        return f"'{self.current_valve.name}' {self.current_valve.open_icon}: {self.current_pressure}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other: Route):
        return self.current_pressure < other.current_pressure

    def __le__(self, other: Route):
        return self.current_pressure <= other.current_pressure

    def __gt__(self, other: Route):
        return self.current_pressure > other.current_pressure

    def __ge__(self, other: Route):
        return self.current_pressure >= other.current_pressure

    @property
    def current_valve(self):
        return self.valves[self._current_valve]

    @property
    def open_valve(self) -> bool:
        return self.current_valve.flow_rate > 0 and not self.current_valve.open

    @property
    def leads_to(self) -> list[Valve]:
        return self.current_valve.leads_to

    def _resolve_open_valves(self) -> None:
        for valve in self.open_valves:
            self.current_pressure += valve.flow_rate

    def _resolve_action(self, next_valve: Valve | None) -> None:
        if next_valve:
            self._current_valve = next_valve.name
        else:
            self.current_valve.open = True
            self.open_valves.append(self.current_valve)

    def run(self, next_valve: Valve | None) -> None:
        assert (
            self.current_valve in self.open_valves if self.current_valve.open else True
        )
        self._resolve_open_valves()
        self._resolve_action(next_valve)


class Cycles:
    def __init__(self, input_: str, total_time: int):
        self._input = input_
        self.total_time = total_time
        self.current_time = 0
        self.routes: list[Route] = [Route(input_)]

    def run(self):
        while self.current_time < self.total_time:
            print(
                f"== Running minute {1 + self.current_time} with {len(self.routes)} routes =="
            )

            extra_routes = []
            remove_routes = []
            for route in self.routes:
                for idx, next_valve in enumerate(route.leads_to, start=1):
                    new_route = copy.deepcopy(route)
                    new_route.run(next_valve=next_valve)
                    new_route.id += str(idx)
                    extra_routes.append(new_route)

                if route.open_valve:
                    route.run(next_valve=None)
                    route.id += "0"
                else:
                    remove_routes.append(route)

            [self.routes.remove(rt) for rt in remove_routes]
            self.routes += extra_routes
            self.routes = sorted(self.routes)[
                -5000:
            ]  # Limit (arbitrarily) otherwise takes way too long
            self.current_time += 1


def solution(input_: str) -> list[Any]:
    """
    Solve the day 16 problem!
    """
    cycles = Cycles(input_=input_.strip(), total_time=30)
    cycles.run()

    return [
        max(rt.current_pressure for rt in cycles.routes),
        0,
    ]
