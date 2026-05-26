SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id)      AS total_orders,
    ROUND(AVG(i.price)::numeric, 2) AS avg_order_value,
    MAX(o.purchased_at)             AS last_order_date,
    ROUND(SUM(i.price)::numeric, 2) AS total_spend
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_customers') }} c ON o.customer_id = c.customer_id
JOIN {{ ref('stg_order_items') }} i ON o.order_id = i.order_id
GROUP BY 1