import pathlib
import sys

import duckdb

HERE = pathlib.Path(__file__).parent


# https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
class Colour:
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    INTENSE_BLACK = "\033[90m"
    INTENSE_RED = "\033[91m"
    INTENSE_GREEN = "\033[92m"
    INTENSE_YELLOW = "\033[93m"
    INTENSE_BLUE = "\033[94m"
    INTENSE_PURPLE = "\033[95m"
    INTENSE_CYAN = "\033[96m"
    INTENSE_WHITE = "\033[97m"


SYMBOL_COLOURS = {
    " ": Colour.ENDC,
    "•": Colour.INTENSE_BLACK,
    "↑": Colour.INTENSE_BLACK,
    "↓": Colour.INTENSE_BLACK,
    "←": Colour.INTENSE_BLACK,
    "→": Colour.INTENSE_BLACK,
    "#": Colour.RED,
    "S": Colour.INTENSE_PURPLE + Colour.BOLD,
    "O": Colour.INTENSE_PURPLE + Colour.BOLD,
    "^": Colour.INTENSE_GREEN,
    "v": Colour.INTENSE_GREEN,
    "<": Colour.INTENSE_GREEN,
    ">": Colour.INTENSE_GREEN,
    "U": Colour.INTENSE_YELLOW,
    "D": Colour.INTENSE_YELLOW,
    "L": Colour.INTENSE_YELLOW,
    "R": Colour.INTENSE_YELLOW,
    "|": Colour.BLUE,
    "-": Colour.BLUE,
    "+": Colour.BLUE,
}

ADJUSTER_SQL = """
    copy (
        with

        orig as (
            select step, x, y, direction, route.replace('.', ' ') as route
            from '{here}/routes.parquet'
            where loop_id = {loop_id}
        ),

        graph as (
            from (
                from orig
                select
                    x as orig_x,
                    y as orig_y,
                    direction as orig_direction,
                    generate_subscripts(split(route, chr(10)), 1) as y,
                    unnest(split(route, chr(10))) as row_part,
            )
            select
                orig_x,
                orig_y,
                orig_direction,
                y,
                generate_subscripts(split(row_part, ''), 1) as x,
                unnest(split(row_part, '')) as cell,
        ),

        neighbours as (
            select
                graph.orig_x,
                graph.orig_y,
                graph.orig_direction,
                graph.x,
                graph.y,
                graph.cell,
                coalesce(east.cell, '') as cell__east,
                coalesce(west.cell, '') as cell__west,
                coalesce(north.cell, '') as cell__north,
                coalesce(south.cell, '') as cell__south,
            from graph
                asof left join graph as east
                    on  graph.y = east.y
                    and graph.x > east.x
                    and east.cell != ' '
                asof left join graph as west
                    on  graph.y = west.y
                    and graph.x < west.x
                    and west.cell != ' '
                asof left join graph as north
                    on  graph.x = north.x
                    and graph.y > north.y
                    and north.cell != ' '
                asof left join graph as south
                    on  graph.x = south.x
                    and graph.y < south.y
                    and south.cell != ' '
        ),

        graph_adj as (
            select
                x,
                y,
                cell,
                (cell__east = '>' or cell__west = '<') as x_flag,
                (cell__north = 'v' or cell__south = '^') as y_flag,
                case
                    when (x, y) = (orig_x, orig_y)
                        then case orig_direction
                            when [ 1,  0] then 'R'
                            when [-1,  0] then 'L'
                            when [ 0,  1] then 'D'
                            when [ 0, -1] then 'U'
                                          else 'X'
                        end
                    when (x, y) = (orig_x + orig_direction[1], orig_y + orig_direction[2])
                        then 'O'
                    when cell in ('#', '>', '<', 'v', '^')
                        then cell
                    when x_flag and y_flag
                        then '+'
                    when x_flag
                        then '-'
                    when y_flag
                        then '|'
                    when (x, y) in (select (x, y) from day_06.original_journey)
                        then (
                            select case directions.symbol
                                when '^' then '↑'
                                when 'v' then '↓'
                                when '<' then '←'
                                when '>' then '→'
                            end
                            from day_06.original_journey
                                inner join day_06.directions
                                    using (direction)
                            where neighbours.x = original_journey.x
                              and neighbours.y = original_journey.y
                            order by original_journey.step desc
                            limit 1
                        )
                        else cell
                end as cell_adj,
            from neighbours
        )

        from (
            select y, string_agg(cell_adj, '' order by x) as graph
            from graph_adj
            group by y
        )
        select string_agg(graph, chr(10) order by y) as route_adj,
    ) to '{here}/routes-adj-{loop_id}.csv' (header false, quote '')
"""


def _colour_char(char: str, colour_map: dict[str, Colour]) -> str:
    col = colour_map.get(char, Colour.ENDC)
    return col + char + Colour.ENDC


def colour_route(route: str, colour_map: dict[str, Colour]) -> str:
    return "".join(_colour_char(char, colour_map) for char in route)


def adjust_route(loop_id: int, conn: duckdb.DuckDBPyConnection) -> None:
    print("Adjusting route...")
    conn.sql(ADJUSTER_SQL.format(loop_id=loop_id, here=HERE.absolute()))
    print("Route adjusted")


def adjust_and_print(loop_id: int, conn: duckdb.DuckDBPyConnection) -> None:
    route = HERE / f"routes-adj-{loop_id}.csv"
    if not route.exists():
        adjust_route(loop_id, conn)

    print(colour_route(route.read_text(encoding="utf-8"), SYMBOL_COLOURS))


def main(from_loop: int, to_loop: int) -> None:
    """
    python -m advent_of_code.solutions.year_2024.day_06.routes.viewer 0
    """
    conn = duckdb.connect(
        # ew
        HERE.parent.parent.parent.parent.parent / "aoc.duckdb"
    )
    for loop_id in range(from_loop, 1 + to_loop):
        adjust_and_print(loop_id, conn)


if __name__ == "__main__":
    if len(sys.argv) == 2:  # noqa: PLR2004
        main(int(sys.argv[1]), int(sys.argv[1]))
    elif len(sys.argv) == 3:  # noqa: PLR2004
        main(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print("This must be called with one or two arguments")
