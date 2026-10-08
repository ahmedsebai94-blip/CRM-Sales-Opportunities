SELECT 
    account AS account_name,
    sector,
    year_established,
    revenue,
    employees,
    office_location,
    subsidiary_of
FROM {{ source('ods', 'accounts') }}