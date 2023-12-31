"""
Hooks to run when building the site documentation.
"""
import contextlib
import os
import re

from advent_of_code.constants import ROOT as SRC_ROOT  # advent_of_code/

DOCS = SRC_ROOT.parent / "docs"
YEARS = {2022, 2023}
DAYS = range(1, 26)


def copy_readme() -> None:
    """
    Copy the ``README.md`` file to ``docs/index.md``.
    """
    contents = (SRC_ROOT.parent / "README.md").read_text(encoding="utf-8")
    without_badges = contents.split("---", maxsplit=1)[1].strip()
    (DOCS / "index.md").write_text(without_badges, encoding="utf-8")


def _read_daily_file(year: int, day: int) -> str:
    with contextlib.suppress(FileNotFoundError):
        path = SRC_ROOT / f"year_{year}/day_{day:02d}/README.md"
        return re.sub(
            r"--- (Day \d+: .+) ---([\S\s]*)",
            r"\1\2\n",
            path.read_text(encoding="utf-8"),
        )


def publish_daily_docs() -> None:
    """
    Publish the daily problem statements.
    """
    for year in YEARS:
        yearly_file = DOCS / f"{year}/index.md"
        os.makedirs(yearly_file.parent, exist_ok=True)
        yearly_file.write_text(f"# {year}\n\n", encoding="utf-8")
        for day in DAYS:
            if daily_file := _read_daily_file(year, day):
                with open(yearly_file, "a", encoding="utf-8") as f:
                    f.write(f"## {daily_file}")


###
# Callbacks
###


def on_startup(**kwargs) -> None:
    """
    Callback which runs per ``mkdocs`` invocation.

    - https://www.mkdocs.org/dev-guide/plugins/#on_startup
    """
    copy_readme()
    publish_daily_docs()
