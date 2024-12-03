with

input(data) as (
    select string_agg(column0)
    from read_csv('{{ file }}', header=false, sep='')
),

expressions as (
    select
        data,
        unnest(regexp_extract_all(
            data,
            'mul\(\d{1,3},\d{1,3}\)'
        )) as expression
    from input
)

from expressions
select sum(1
    * regexp_replace(
        expression,
        'mul\((\d{1,3}),(\d{1,3})\)',
        '\1'
    )::int
    * regexp_replace(
        expression,
        'mul\((\d{1,3}),(\d{1,3})\)',
        '\2'
    )::int
) as solution
;
