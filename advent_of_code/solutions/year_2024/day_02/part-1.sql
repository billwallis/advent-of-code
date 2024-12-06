with

input(data) as (
    select *
    from read_csv('{{ file }}', header=false)
),

reports as (
    from (
        select
            data,
            row_number() over () as report_id,
            split(data, ' ') as report,
        from input
    )
    select
        report_id,
        unnest(report)::int as level,
        generate_subscripts(report, 1) AS index,
),

report_flags as (
    from (
        select
            report_id,
            level,
            lag(level) over (partition by report_id order by index) as previous_level,
            level - previous_level as difference,
        from reports
        qualify previous_level is not null
        order by report_id, index
    )
    select
        report_id,
        count(distinct sign(difference)) = 1 as is_monotonic,
        max(abs(difference)) <= 3 as is_bounded_above,
        min(abs(difference)) >= 1 as is_bounded_below,
    group by report_id
)


select count(*)
from report_flags
where 1=1
    and is_monotonic
    and is_bounded_above
    and is_bounded_below
;
