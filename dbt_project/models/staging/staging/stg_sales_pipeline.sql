SELECT
    opportunity_id,
    sales_agent,
    product AS product_name,
    account AS account_name,
    deal_stage,
    engage_date::DATE as engage_date,
    close_date::DATE as close_date,
    close_value
FROM {{ source('ods', 'sales_pipeline') }}