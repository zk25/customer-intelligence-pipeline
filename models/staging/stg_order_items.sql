SELECT
    order_id,
    product_id,
    CAST(price AS FLOAT) AS price,
    CAST(freight_value AS FLOAT) AS freight_value
FROM {{ ref('olist_order_items_dataset') }}