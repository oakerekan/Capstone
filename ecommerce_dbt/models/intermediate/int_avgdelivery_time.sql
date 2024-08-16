-- models/intermediate/int_avg_delivery_time.sql
with delivery_times as (
    select
        order_id,
        order_date,
        delivery_date,
        date_diff(delivery_date, order_date, day) as delivery_time
    from {{ ref('stg_orders') }}
)
select
    avg(delivery_time) as avg_delivery_time
from delivery_times
