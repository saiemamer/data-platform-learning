{{ config(
    materialized='view',
    persist_docs={"relation": true, "columns": true}
) }}

select
    station_id,
    name,
    status
from {{ source('my_platform_sources', 'bikeshare_stations') }}
