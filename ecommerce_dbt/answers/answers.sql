select
    category,
    total_sales
from {{ ref('fct_sales_by_category') }}
order by total_sales desc;



select
    avg_delivery_time
from {{ ref('fct_avg_delivery_time') }};



select
    state,
    total_orders
from {{ ref('fct_orders_by_state') }}
order by total_orders desc;