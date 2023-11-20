"""
Profile the OOP and the optimal solutions.
"""
from typing import Callable

import profiler


def profile(oop_solution: Callable, optimal_solution: Callable, repeat: int) -> None:
    """
    Profile different solutions.
    """
    functions = {
        "oop": oop_solution,
        "optimal": optimal_solution,
    }
    profiler.time_functions(functions, repeat)
