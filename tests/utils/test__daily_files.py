"""
Tests for the ``advent_of_code/utils/daily_files.py`` module.
"""

import pathlib

import pytest

import advent_of_code.utils.daily_files as daily_files
from advent_of_code.constants import ROOT


@pytest.fixture
def root(tmp_path: pathlib.Path) -> pathlib.Path:
    """
    Return a temporary directory.
    """
    global ROOT  # Dirty hack, but I don't know how to do it better
    ROOT = tmp_path

    return ROOT
