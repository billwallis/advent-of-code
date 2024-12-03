with

input(data) as (
    select string_agg(column0)
    from read_csv('{{ file }}', header=false, sep='')
),

expressions as (
    from input
    select
        regexp_replace(data, 'don''t\(\).*?(do\(\)|$)', '', 'g') as instructions,
        unnest(regexp_extract_all(
            instructions,
            'mul\(\d{1,3},\d{1,3}\)'
        )) as expression
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
