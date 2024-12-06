with recursive

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

/* Brute force through the indexes */
reports_without_index(without_index, report_id, report, is_safe) as (
        select -1, null::int, null::int[], null::bool
    union all
        select
            without_index_,
            report_id,
            report,
            is_safe,
        from (
            select
                without_index_,
                report_id,
                list(level) as report,
                count(distinct sign(difference)) = 1 as is_monotonic,
                max(abs(difference)) <= 3 as is_bounded_above,
                min(abs(difference)) >= 1 as is_bounded_below,
                (1=1
                    and is_monotonic
                    and is_bounded_above
                    and is_bounded_below
                ) as is_safe,
            from (
                select
                    meta.without_index_,
                    reports.report_id,
                    reports.level,
                    lag(reports.level) over (
                        partition by reports.report_id
                        order by reports.index
                    ) as previous_level,
                    reports.level - previous_level as difference,
                from reports
                    cross join (
                        select max(without_index) + 1 as without_index_,
                        from reports_without_index
                        having without_index_ <= (select max(index) from reports)
                    ) as meta
                where reports.index != meta.without_index_
            )
            group by without_index_, report_id
        )
)

select count(distinct report_id)
from reports_without_index
where is_safe
;
