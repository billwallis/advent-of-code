"""
Create the template files for the daily problems.
"""
import datetime
import os.path


class FileCreator:
    """
    Create the template files for the daily problems.
    """

    def __init__(self, day: int):
        self.day = day
        self.directory = os.path.join("advent_of_code", f"day_{day}")

    def filepath(self, file: str) -> str:
        """
        Return the filepath for the file at the directory corresponding to the
        daily problem.
        """
        return os.path.join(self.directory, file)

    def write_to_file(self, filename: str, contents: str) -> None:
        """
        Write the contents to a file.

        Creates the file if it doesn't already exist.
        """
        with open(self.filepath(filename), "w+") as f:
            f.write(contents)

    def create_files(self) -> None:
        """
        Create the daily directory and all of its files.
        """
        self._create_directory()
        self._create_init()
        self._create_oop()
        self._create_optimal()
        self._create_readme()

    def _create_directory(self) -> None:
        os.makedirs(self.directory)

    def _create_init(self) -> None:
        contents = f'''
        """
        Day {self.day}:

        https://adventofcode.com/2022/day/{self.day}/input
        """
        from advent_of_code.day_{self.day}.oop import solution as solution_oop
        from advent_of_code.day_{self.day}.optimal import solution as solution_optimal


        SAMPLE_INPUT = """
        """
        '''.replace(
            "        ", ""
        )

        self.write_to_file(
            filename="__init__.py",
            contents=contents[1:],
        )

    def _create_oop(self) -> None:
        contents = f'''
        """
        OOP solution for day {self.day}.
        """
        from typing import Any


        def solution(input_: str) -> list[Any]:
            """
            Solve the day {self.day} problem!
            """

            return [0, 0]
        '''.replace(
            "        ", ""
        )

        self.write_to_file(
            filename="oop.py",
            contents=contents[1:],
        )

    def _create_optimal(self) -> None:
        contents = f'''
        """
        Optimal (?) solution for day {self.day}.
        """
        from typing import Any


        def solution(input_: str) -> list[Any]:
            """
            Solve the day {self.day} problem!
            """

            return [0, 0]
        '''.replace(
            "        ", ""
        )

        self.write_to_file(
            filename="optimal.py",
            contents=contents[1:],
        )

    def _create_readme(self) -> None:
        contents = f"""
        --- Day {self.day}:  ---

        ### Part One


        ### Part Two

        """.replace(
            "        ", ""
        )

        self.write_to_file(
            filename="README.md",
            contents=contents[1:],
        )


def create_files(day: int = None) -> None:
    """
    Create the template files for the day.
    """
    day = day or datetime.datetime.now().day
    file_creator = FileCreator(day)
    file_creator.create_files()
