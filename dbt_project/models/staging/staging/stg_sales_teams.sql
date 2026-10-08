SELECT
    sales_agent,
    manager,
    regional_office
FROM {{ source('ods', 'sales_teams') }}