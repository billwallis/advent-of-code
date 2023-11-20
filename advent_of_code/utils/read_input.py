"""
Function to read the inputs.
"""
import os.path


def read_input(module: str) -> str:
    """
    Open the input file and return its contents.
    """
    with open(os.path.join("advent_of_code", module, "input.csv")) as f:
        return f.read()
