
with raw_products as (
    select * from {{ source('ecommerce', 'products') }}
)
select
    product_id,
    product_name,
    category
from raw_products
