SELECT
    opportunity_id,
    sales_agent,
    product_name,
    account_name,
    deal_stage,
    engage_date,
    close_date,
    close_value,
    DATEDIFF('day', engage_date, close_date) as days_to_close
FROM {{ ref('stg_sales_pipeline') }}