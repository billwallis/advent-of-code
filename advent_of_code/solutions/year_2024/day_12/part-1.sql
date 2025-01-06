with recursive

input(data) as (
    select *
    from read_csv('advent_of_code/solutions/year_2024/day_12/sample-3.data', header=false)
    -- from read_csv('advent_of_code/solutions/year_2024/day_12/input.data', header=false)
),

grid as (
    from input
    select
        generate_subscripts(split(data, ''), 1) as x,
        row_number() over () as y,
        unnest(split(data, '')) as plant,
),

directions(direction) as (
    values
        ([ 0, -1]),
        ([ 1,  0]),
        ([ 0,  1]),
        ([-1,  0]),
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

region_edges__right_down as (
        select
            grid.plant,
            'right' as edge_type,
            [grid.x, grid.y] as point_1,
            [r.x, r.y] as point_2,
        from grid
            inner join grid as r
                on  grid.x + 1 = r.x
                and grid.y = r.y
                and grid.plant = r.plant
    union all
        select
            grid.plant,
            'down' as edge_type,
            [grid.x, grid.y] as point_1,
            [d.x, d.y] as point_2,
        from grid
            inner join grid as d
                on  grid.x = d.x
                and grid.y + 1 = d.y
                and grid.plant = d.plant
),

region_edges as (
        select plant, edge_type, point_1, point_2
        from region_edges__right_down
    union all
        select plant, if(edge_type = 'down', 'up', 'left'), point_2, point_1
        from region_edges__right_down
),

regions(i, region_id, region, point, seen) as (
        select 0, uuid(), plant, [x, y], [[x, y]]
        from grid
    union all (
        with next_points as (
            from (
                select
                    regions.i + 1 as i,
                    regions.region_id,
                    regions.region,
                    region_edges.point_2 as point,
                    regions.seen,
                from regions
                    inner join region_edges
                        on  regions.point = region_edges.point_1
                        and not regions.seen.list_contains(region_edges.point_2)
            )
            select
                i,
                region_id,
                region,
                point,
                (seen
                    .list_concat(list(point) over (partition by region_id))
                    .list_distinct()
                    .list_sort()
                ) as seen,
        )

        /* If region IDs overlap (intersection in `seen`), combine them */
        from next_points
        -- select
        --     i,
        --     (
        --         select min(region_id)
        --         from next_points as innr
        --         /* Only one depth of intersection */
        --         where list_intersect(next_points.seen, innr.seen) != []
        --     ),
        --     region,
        --     point,
        --     seen,
    )
),

region_areas as (
    from (
        select region_id, region, seen
        from regions
        qualify i = max(i) over (partition by region_id)
    )
    select
        seen,
        any_value(region) as region,
        any_value(region_id) as region_id,
        len(seen) as area,
    group by seen
),

region_perimeters as (
    from (
        from region_areas
        select
            region_id,
            unnest(seen)[1] as x,
            unnest(seen)[2] as y,
    ) inner join perimeters using (x, y)
    select
        region_id,
        sum(perimeter) as perimeter,
    group by region_id
)

select sum(area * perimeter)
from region_areas
    inner join region_perimeters
        using (region_id)
;
