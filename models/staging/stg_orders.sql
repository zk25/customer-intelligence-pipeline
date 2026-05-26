SELECT
    order_id,
    customer_id,
    order_status,
    CAST(order_purchase_timestamp AS TIMESTAMP) AS purchased_at,
    CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_at
FROM {{ ref('olist_orders_dataset') }}
WHERE order_status = 'delivered'