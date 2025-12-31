select
    station_id,
    name,
    status
from {{ source('my_platform_sources', 'bikeshare_stations') }}