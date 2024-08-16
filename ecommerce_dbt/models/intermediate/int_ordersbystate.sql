-- models/intermediate/int_orders_by_state.sql
with orders as (
    select
        state,
        count(order_id) as total_orders
    from {{ ref('stg_orders') }}
    group by state
)
select
    state,
    total_orders
from orders
