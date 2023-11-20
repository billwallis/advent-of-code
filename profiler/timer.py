"""
Profile some functions.
"""
import dataclasses
import datetime
import functools
import timeit
from typing import Any, Callable

import rich
import tqdm


@dataclasses.dataclass
class Runner:
    """
    Callable object representing a function.

    Wrapped into an object rather than left as a function to assign additional
    properties to the functions, making them easier to monitor and summarise
    their statistics.
    """

    runner: Callable
    name: str
    repeat: int = 0
    total_time: float = 0.0

    def __call__(self, time_it: bool = True):
        if time_it:
            self.repeat += 1
            self.total_time += timeit.timeit(self.runner, number=1)
        else:
            self.runner()

    @property
    def average_time(self) -> float:
        """
        The average time that this function has taken to run.
        """
        return self.total_time / self.repeat


def create_runners(functions: dict[str, Callable]) -> list[Runner]:
    """
    Create a list of Runners each corresponding to a function.
    """
    return [Runner(runner=func, name=name) for name, func in functions.items()]


def print_runner_stats(list_of_runners: list[Runner]) -> None:
    """
    Print the average run times of the runners in ``list_of_runners``.
    """
    total_avg_time = sum(runner.average_time for runner in list_of_runners)
    for runner in list_of_runners:
        print(
            f"{runner.name}: {runner.average_time:.8f} ({runner.average_time / total_avg_time:.1%})",
        )


def print_times() -> Callable:
    """
    Decorator to print the start and end times of the wrapped function.

    For the colours from the ``rich`` package, make sure that the run
    configuration in PyCharm has the "Emulate terminal in output console"
    checkbox toggled on.

    See more at:

    - https://rich.readthedocs.io/en/stable/introduction.html
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            rich.print(f"[blue]Start time: {datetime.datetime.now()}[/blue]")
            func(*args, **kwargs)
            rich.print(f"[blue]End time: {datetime.datetime.now()}[/blue]")

        return wrapper

    return decorator


@print_times()
def time_functions(functions: dict[str, Callable], repeat: int) -> None:
    """
    Time the queries, running them each ``repeat`` number of times.
    """
    runners: list[Runner] = create_runners(functions=functions)

    for _ in tqdm.trange(repeat):
        for runner in runners:
            runner()

    print_runner_stats(list_of_runners=runners)
