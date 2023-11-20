"""
OOP solution for day 7.
"""
from __future__ import annotations

import json
from typing import Any, Generator


def _is_command(line: str) -> bool:
    return line.startswith("$")


def _is_directory(line: str) -> bool:
    return line.startswith("dir")


class Encoder(json.JSONEncoder):
    """
    Encoder to serialise objects to JSON that aren't supported by JSON.
    """

    def default(self, obj: Any) -> str:
        """
        Return the repr of the object.
        """
        return repr(obj)


class File:
    """
    A file, which only has a size.
    """

    def __init__(self, size: int):
        self.size = size

    def __str__(self):
        return str(self.size)

    def __repr__(self):
        return str(self.size)


class Directory(dict):
    """
    A directory, which is a dict-like object.

    It has a root, a parent, and may have children which are files and other
    directories.
    """

    def __init__(self, root: Directory, parent: Directory):
        super().__init__()
        self.root = root
        self.parent = parent

    def to_directory(self, dir_name: str) -> Directory:
        """
        Navigate to a given directory relative to this directory.
        """
        match dir_name:
            case "/":
                return self.root
            case "..":
                return self.parent
            case _:
                return self[dir_name]

    def add_directory(self, dir_name: str) -> Directory:
        """
        Add a child directory to this directory.
        """
        if dir_name in self:
            raise ValueError(f"There already exists an object called {dir_name}")

        self[dir_name] = Directory(root=self.root, parent=self)
        return self[dir_name]

    def add_file(self, file_name: str, file_size: int) -> None:
        """
        Add a child file to this directory.
        """
        self[file_name] = File(file_size)

    @property
    def size(self) -> int:
        """
        The total size taken up by the directory.
        """
        return sum(item.size for item in self.values())


class Root(Directory):
    """
    A root directory, which is a special case of a directory.
    """

    def __init__(self):
        super().__init__(root=self, parent=None)  # noqa


class FileSystem:
    """
    A file system, which is a set of directories.
    """

    def __init__(
        self,
        structure: dict[str, Directory[str, File | Directory]],
        total_disk_space: int,
    ):
        self.structure = structure
        self.total_disk_space = total_disk_space
        self.required_disk_space: int = 0

    def __str__(self):
        return json.dumps(self.structure, indent=4, cls=Encoder)

    @classmethod
    def from_output_string(cls, text: str, total_disk_space: int) -> FileSystem:
        """
        Parse the console output into a file system.
        """
        output = text.split("\n")
        root = Root()
        is_ls = False
        curr_dir = root

        for row in output:
            if _is_command(row):
                commands = row.split()
                match commands[1]:
                    case "ls":
                        is_ls = True
                    case "cd":
                        is_ls = False
                        curr_dir = curr_dir.to_directory(commands[2])
            else:
                assert is_ls
                details = row.split()
                if _is_directory(row):
                    curr_dir.add_directory(details[1])
                else:
                    curr_dir.add_file(file_name=details[1], file_size=int(details[0]))

        return cls(structure={"/": root}, total_disk_space=total_disk_space)

    def _get_directory_sizes(self, directory: Directory) -> Generator:
        """
        Get the directory sizes.
        """
        for name, contents in directory.items():
            if isinstance(contents, Directory):
                yield name, contents.size
                yield from self._get_directory_sizes(contents)

    def sum_directories_less_than(self, max_size: int) -> int:
        """
        Get the directories and their sizes for the directories whose size is
        less than or equal to the input size.
        """
        return sum(
            size
            for dir_name, size in self._get_directory_sizes(self.structure)  # noqa
            if size <= max_size
        )

    def find_smallest_required_dir(self) -> int:
        """
        Find the smallest directory that, if deleted, would free up enough space
        on the filesystem to run the update.
        """
        reclaim = self.structure["/"].size - (
            self.total_disk_space - self.required_disk_space
        )
        if reclaim < 0:
            return 0  # Already have enough space

        return min(
            size
            for dir_name, size in self._get_directory_sizes(self.structure)  # noqa
            if size >= reclaim
        )


def solution(input_: str) -> list[Any]:
    """
    Solve the day 7 problem!
    """
    file_system = FileSystem.from_output_string(
        text=input_.strip(),
        total_disk_space=70_000_000,
    )
    file_system.required_disk_space = 30_000_000

    return [
        file_system.sum_directories_less_than(100_000),
        file_system.find_smallest_required_dir(),
    ]
