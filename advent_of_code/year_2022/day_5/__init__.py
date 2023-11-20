"""
Day 5: Supply Stacks

https://adventofcode.com/2022/day/5/input
"""
from advent_of_code.year_2022.day_5.oop import solution as solution_oop
from advent_of_code.year_2022.day_5.optimal import solution as solution_optimal

SAMPLE_INPUT = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""[
    1:
]  # Drop the first new line
