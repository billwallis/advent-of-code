/*
    Works for the sample, but not sure about the input yet -- ran for 2+ hours!
*/
set enable_progress_bar = true;


create schema if not exists day_06;
use day_06;


create or replace table day_06.directions as
    from (
    values
        ('^', [ 0, -1], [ 1,  0]),
        ('>', [ 1,  0], [ 0,  1]),
        ('v', [ 0,  1], [-1,  0]),
        ('<', [-1,  0], [ 0, -1]),

    ) as v(symbol, direction, rotate_90)
;
-- from directions;


create or replace table day_06.grid as
    from read_csv('{{ file }}', header=false)
    select
        generate_subscripts(split(column0, ''), 1) AS x,
        row_number() over () as y,
        unnest(split(column0, '')) as cell,
;
-- from grid;


/* ~30s */
create or replace table day_06.original_journey as

/* While the guard is in the map, continue their journey */
with recursive journey as (
        select
            directions.direction,
            grid.x,
            grid.y,
            1 as step,
        from grid
            inner join directions
                on grid.cell = directions.symbol
    union all
        from (
            select
                journey.*,
                if(front.cell = '#', 'turn', 'move') as action,
                directions.rotate_90,
            from journey
                inner join directions
                    using (direction)
                inner join grid as front
                    on  journey.x + journey.direction[1] = front.x
                    and journey.y + journey.direction[2] = front.y
        )
        select
            if(action = 'turn', rotate_90, direction),
            if(action = 'turn', x, x + direction[1]) as x_,
            if(action = 'turn', y, y + direction[2]) as y_,
            step + 1,
        where (x_, y_) in (select (x, y) from grid)
)

from journey
;


from original_journey;


/* should be 4374 */
from original_journey
select count(distinct (x, y))
;


create or replace table day_06.simulated_journeys as

/* For each step, re-calculate with an obstruction in front */
from (
    from day_06.original_journey
    select
        *,
        {'x': x + direction[1], 'y': y + direction[2], cell: '#'} as next_step,
    where 1=1
        /* only where the next step is in the grid */
        and (next_step['x'], next_step['y']) in (select (x, y) from grid)
        /* we can skip the ones where the next step would already be an obstruction */
        and (next_step['x'], next_step['y'], next_step['cell']) not in (select (x, y, cell) from grid)
) as orig
select
    step,
    direction,
    x,
    y,
    next_step,
    (
        with recursive

        /* Make the next step an obstruction */
        grid_adj as (
            from day_06.grid
            select * replace (
                if(
                    (x, y) = (orig.next_step['x'], orig.next_step['y']),
                    orig.next_step['cell'],
                    cell
                ) as cell
            )
        ),

        journey_adj as (
                /* Reference outer query to make this correlated */
                select
                    orig.direction,
                    orig.x,
                    orig.y,
                    [(orig.direction, orig.x, orig.y)] as seen,
                    false as is_loop,
            union all
                from (
                    select
                        journey_adj.*,
                        case coalesce((
                            select cell
                            from grid_adj
                            where journey_adj.x + journey_adj.direction[1] = grid_adj.x
                              and journey_adj.y + journey_adj.direction[2] = grid_adj.y
                        ), 'X')
                            when '#' then 'turn'
                            when 'X' then 'stop'
                                     else 'move'
                        end as action,
                        directions.rotate_90,
                    from journey_adj
                        inner join day_06.directions
                            using (direction)
                    where 1=1
                        and not journey_adj.is_loop
                        and action != 'stop'
                )
                select
                    if(action = 'turn', rotate_90, direction) as direction_,
                    if(action = 'turn', x, x + direction[1]) as x_,
                    if(action = 'turn', y, y + direction[2]) as y_,
                    list_append(seen, (direction_, x_, y_)),
                    list_contains(seen, (direction_, x_, y_)),
                where (x_, y_) in (select (x, y) from grid)
        )

        select max(is_loop)
        from journey_adj
    ) as is_loop,
;


/* should be 1705 */
select
    count(distinct next_step),
    count(distinct (next_step['x'], next_step['y'])),
from day_06.simulated_journeys
where is_loop
;
