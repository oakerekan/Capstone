-- models/intermediate/int_sales_by_category.sql
with sales as (
    select
        o.product_id,
        p.category,
        sum(o.quantity * o.price) as total_sales
    from {{ ref('stg_orders') }} o
    join {{ ref('stg_products') }} p
    on o.product_id = p.product_id
    group by p.category
)
select
    category,
    total_sales
from sales
