with recursive

input(data) as (
    select *
    from read_csv('{{ file }}', header=false)
),

/*
    x increments right (->)
    y increments down (v)
*/
grid as (
    select
        generate_subscripts(split(data, ''), 1) AS x,
        row_number() over () as y,
        unnest(split(data, '')) as cell,
    from input
),

directions(direction, rotate_90) as (
    values
        ([ 0, -1], [ 1,  0]),
        ([ 1,  0], [ 0,  1]),
        ([ 0,  1], [-1,  0]),
        ([-1,  0], [ 0, -1]),
),

/* While the guard is in the map, continue their journey */
journey as (
        select
            case cell
                when '^' then [0, -1]
                when '>' then [1, 0]
                when 'v' then [0, 1]
                when '<' then [-1, 0]
            end as direction,
            x,
            y,
        from grid
        where cell in ('^', '>', 'v', '<')
    union all
        from (
            from journey
            select
                *,
                if(
                    /* Is the next cell an obstruction (#) */
                    exists(
                        select *
                        from grid as front
                        where 1=1
                            and (journey.x + journey.direction[1]) = front.x
                            and (journey.y + journey.direction[2]) = front.y
                            and front.cell = '#'
                    ),
                    (
                        select rotate_90
                        from directions
                        where directions.direction = journey.direction
                    ),
                    direction
                ) as direction_
        )
        select
            direction_,
            x + direction_[1] as x_,
            y + direction_[2] as y_,
        where (x_, y_) in (select (x, y) from grid)
)

from journey
select count(distinct (x, y))
;
