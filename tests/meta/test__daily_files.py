"""
Tests for the ``advent_of_code/meta/daily_files.py`` module.
"""

import pathlib

import pytest

from advent_of_code.meta import daily_files


def _read_fixture(name: str) -> str:
    path = pathlib.Path(__file__).parent / "fixtures" / name
    return path.read_text("utf-8").strip()


def test__files_can_be_created(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
):
    year, day = 2020, 1
    monkeypatch.setattr(daily_files, "SOLUTIONS_ROOT", tmp_path)
    daily_files.create_files(year, day)

    assert (tmp_path / f"year_{year}/day_{day:02d}").exists()
    assert (tmp_path / f"year_{year}/day_{day:02d}/main.py").exists()
    assert (tmp_path / f"year_{year}/day_{day:02d}/sample.data").exists()

    main_content = (
        (tmp_path / f"year_{year}/day_{day:02d}/main.py").read_text().strip()
    )
    assert main_content == _read_fixture("mock_main.py")
