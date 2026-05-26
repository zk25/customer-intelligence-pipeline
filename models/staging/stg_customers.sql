SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state
FROM {{ ref('olist_customers_dataset') }}