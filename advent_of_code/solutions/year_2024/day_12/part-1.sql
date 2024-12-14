with recursive

input(data) as (
    select *
    from read_csv('advent_of_code/solutions/year_2024/day_12/sample-3.data', header=false)
),

grid as (
    from input
    select
        generate_subscripts(split(data, ''), 1) as x,
        row_number() over () as y,
        unnest(split(data, '')) as plant
),

directions(direction) as (
    values
        ([ 0, -1]),
        ([ 1,  0]),
        ([ 0,  1]),
        ([-1,  0]),
),

right_down(direction) as (
    values
        ([ 1,  0]),
        ([ 0,  1]),
),

/* Loop to compute the perimeter */
perimeters(x, y, plant, perimeter) as (
    from (
        from grid as o  /* outer */
            cross join directions
        select
            x,
            y,
            plant,
            direction,
            1 - exists(
                select *
                from grid as i  /* inner */
                where (o.x + direction[1], o.y + direction[2], o.plant) = (i.x, i.y, i.plant)
            )::int as perimeter_contribution
    )
    select x, y, any_value(plant), sum(perimeter_contribution)
    group by x, y
),

-- /* Recurse to join regions together */
-- regions(x, y, plant, plot_id) as (
--         select x, y, plant, uuid()
--         from grid
--         where (x, y) = (1, 1)
--     union all
--         select
--             grid.x,
--             grid.y,
--             grid.plant,
--             coalesce(
--                 (
--                     select any_value(plot_id)
--                     from regions
--                     where (grid.x, grid.y, grid.plant) in (
--                         (regions.x + 1, regions.y,     regions.plant),
--                         (regions.x,     regions.y + 1, regions.plant),
--                     )
--                 ),
--                 uuid()
--             ),
--         from grid
--         where exists(
--             select *
--             from regions
--             where (grid.x, grid.y) in (
--                 (regions.x + 1, regions.y),      /* match one right */
--                 (regions.x,     regions.y + 1),  /* match one down */
--             )
--         )
-- )

-- /* Recurse to join regions together */
-- regions(plot_id, x, y, plant, _seen, i) as (
--         from (
--             select
--                 *,
--                 plant != lag(plant, 1, '') over (partition by x order by y) as x_flag,
--                 plant != lag(plant, 1, '') over (partition by y order by x) as y_flag,
--             from grid
--         )
--         select uuid(), x, y, plant, [(x, y)], 1
--         where x_flag and y_flag
--     union all
--         select
--             regions.plot_id,
--             grid.x,
--             grid.y,
--             grid.plant,
--             list_append(regions._seen, (grid.x, grid.y)),
--             i + 1,
--         from regions
--             cross join right_down
--             inner join grid
--                 on  regions.x + direction[1] = grid.x
--                 and regions.y + direction[2] = grid.y
--                 and regions.plant = grid.plant
--         where not list_contains(regions._seen, (grid.x, grid.y))
-- )

/* Recurse to join regions together */
regions(plot_id, locations) as (
        select null::uuid, null::int[][]
    union all
        select
            regions.plot_id,
            grid.x,
            grid.y,
            grid.plant,
            list_append(regions._seen, (grid.x, grid.y)),
            i + 1,
        from regions
            cross join right_down
            inner join grid
                on  regions.x + direction[1] = grid.x
                and regions.y + direction[2] = grid.y
                and regions.plant = grid.plant
        where not list_contains(regions._seen, (grid.x, grid.y))
)

from regions
select *, unnest(_seen)
order by y, x, generate_subscripts(_seen, 1)

-- from (
--     select
--         regions.plot_id,
--         any_value(regions.plant) as plant,
--         count(*) as area,
--         sum(perimeters.perimeter) as perimeter
--     from regions
--         inner join perimeters
--             using (x, y)
--     group by regions.plot_id
-- )
-- -- select sum(area * perimeter)
--
-- select *
-- order by plant
;
