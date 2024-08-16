
with raw_orders as (
    select * from {{ source('ecommerce', 'orders') }}
)
select
    order_id,
    order_date,
    product_id,
    quantity,
    price
from raw_orders
