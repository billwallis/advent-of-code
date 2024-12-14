with

input(data) as (
    select *
    from read_csv('advent_of_code/solutions/year_{{ year }}/day_{{ "%02d" % day }}/sample.data', header=false)
)

from input
;
