SELECT
    product AS product_name,
    series,
    sales_price
FROM {{ source('ods', 'products') }}