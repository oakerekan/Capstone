
-- Create schema
CREATE SCHEMA IF NOT EXISTS Brazilian_ecommerce;

-- create and populate tables
create table if not exists Brazilian_ecommerce.customers
(
    customer_id varchar not null primary key,
    customer_unique_id varchar,
    customer_zip_code_prefix numeric not null,
    customer_city varchar not null,
    customer_state varchar(2)
);


COPY Brazilian_ecommerce.customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
FROM '/data/olist_customers_dataset.csv' DELIMITER ',' CSV HEADER;

--create geolocation table andcopy data from csv
Create table if not exists Brazilian_ecommerce.geolocation
(
    geolocation_zip_code_prefix numeric not null,
    geolocation_lat numeric not null,
    geolocation_lng numeric not null,
    geolocation_city varchar not null,
    geolocation_state varchar(2)
);

COPY Brazilian_ecommerce.geolocation (geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state)
FROM '/data/olist_geolocation_dataset.csv' DELIMITER ',' CSV HEADER;


-- create order_items and copy data from csv
create table if not exists Brazilian_ecommerce.order_items
(
    order_id varchar not null,
    order_item_id numeric not null,
    product_id varchar not null,
    seller_id varchar not null,
    shipping_limit_date timestamp,
    price numeric not null,
    freight_value numeric not null
);

COPY Brazilian_ecommerce.order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value)
FROM '/data/olist_order_items_dataset.csv' DELIMITER ',' CSV HEADER;


-- create order_payments and copy data from csv
create table if not exists Brazilian_ecommerce.order_payments
(
    order_id varchar not null,
    payment_sequential numeric not null,
    payment_type varchar not null,
    payment_installments numeric not null,
    payment_value numeric not null
);

COPY Brazilian_ecommerce.order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value)
FROM '/data/olist_order_payments_dataset.csv' DELIMITER ',' CSV HEADER;


-- create order_reviews and copy data from csv
create table if not exists Brazilian_ecommerce.order_reviews
(
    review_id varchar not null,
    order_id varchar not null,
    review_score numeric not null,
    review_comment_title varchar,
    review_comment_message varchar,
    review_creation_date timestamp,
    review_answer_timestamp timestamp
);

COPY Brazilian_ecommerce.order_reviews (review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp)
FROM '/data/olist_order_reviews_dataset.csv' DELIMITER ',' CSV HEADER;


-- create orders and copy data from csv  
create table if not exists Brazilian_ecommerce.orders
(
    order_id varchar not null primary key,
    customer_id varchar not null,
    order_status varchar not null,
    order_purchase_timestamp timestamp,
    order_approved_at timestamp,
    order_delivered_carrier_date timestamp,
    order_delivered_customer_date timestamp,
    order_estimated_delivery_date timestamp
);

COPY Brazilian_ecommerce.orders (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date)
FROM '/data/olist_orders_dataset.csv' DELIMITER ',' CSV HEADER;


-- create products and copy data from csv
create table if not exists Brazilian_ecommerce.products
(
    product_id varchar not null primary key,
    product_category_name varchar,
    product_name_lenght numeric,
    product_description_lenght numeric,
    product_photos_qty numeric,
    product_weight_g numeric,
    product_length_cm numeric,
    product_height_cm numeric,
    product_width_cm numeric
);

COPY Brazilian_ecommerce.products (product_id, product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm)
FROM '/data/olist_products_dataset.csv' DELIMITER ',' CSV HEADER;

-- create sellers and copy data from csv

create table if not exists Brazilian_ecommerce.sellers
(
    seller_id varchar not null primary key,
    seller_zip_code_prefix numeric not null,
    seller_city varchar not null,
    seller_state varchar(2)
);

COPY Brazilian_ecommerce.sellers (seller_id, seller_zip_code_prefix, seller_city, seller_state)
FROM '/data/olist_sellers_dataset.csv' DELIMITER ',' CSV HEADER;


-- create product_category_name_translation and copy data from csv
create table if not exists Brazilian_ecommerce.product_category_name_translation
(
    product_category_name varchar not null primary key,
    product_category_name_english varchar not null
);

COPY Brazilian_ecommerce.product_category_name_translation (product_category_name, product_category_name_english)
FROM '/data/product_category_name_translation.csv' DELIMITER ',' CSV HEADER;


