SELECT
    customer_unique_id,
    total_orders,
    avg_order_value,
    total_spend,
    last_order_date,
    CASE
        WHEN total_spend > 500 THEN 'High Value'
        WHEN total_spend > 200 THEN 'Mid Value'
        ELSE 'Low Value'
    END AS segment
FROM {{ ref('int_customer_orders') }}