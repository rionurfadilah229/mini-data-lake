{{ config(materialized='external', location='../data/gold/gempa_harian.parquet') }}

select
    cast(event_time_utc at time zone 'Asia/Jakarta' as date) as tanggal_wib,
    count(*) as jumlah_gempa,
    round(avg(magnitude), 2) as rata_magnitude,
    max(magnitude) as magnitude_max,
    count(*) filter (where tsunami_potential) as jumlah_potensi_tsunami
from {{ source('silver', 'gempa') }}
group by 1
order by 1 desc