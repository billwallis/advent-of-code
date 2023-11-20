"""
Day 7: No Space Left On Device

https://adventofcode.com/2022/day/7/input
"""
from advent_of_code.year_2022.day_7.oop import solution as solution_oop
from advent_of_code.year_2022.day_7.optimal import solution as solution_optimal

SAMPLE_INPUT = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
