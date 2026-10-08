SELECT
    "Table" as table_name,
    "Field" as field_name,
    "Description" as description
FROM {{ source('ods', 'data_dictionary') }}