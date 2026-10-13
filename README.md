![CI](https://github.com/rionurfadilah229/mini-data-lake/actions/workflows/ci.yml/badge.svg)


**Mini Data Lake: Indonesian Earthquake Data (BMKG)**

A small end-to-end data pipeline that pulls recent earthquake data from the public BMKG API, cleans it, and aggregates it into a daily summary table. The project follows a medallion architecture (bronze, silver, gold), stores data as Parquet files, and uses DuckDB with dbt for the analytical layer. Everything runs locally with no cloud account required.

**Pipeline overview**

BMKG API -> bronze (raw JSON) -> silver (cleaned Parquet) -> gold (daily aggregates, Parquet)

**Layers**

Bronze: the raw JSON response from the API, saved as-is with a timestamp in the filename. Keeping the raw data means any later transformation can be re-run from scratch.

Silver: produced by `src/transform.py`. It flattens the nested JSON, converts string fields into proper types (magnitude, depth, coordinates), normalizes event time to UTC, derives a tsunami potential flag, and removes duplicate events that appear across multiple bronze files.

Gold: produced by the dbt model `gempa_harian`. It aggregates silver data per day in Western Indonesia Time (WIB), with the number of earthquakes, average and maximum magnitude, and the number of events with tsunami potential.

**Tech stack**

Python (requests, pandas, pyarrow), Parquet, DuckDB, dbt (dbt-duckdb), pytest, Git.


**Data quality**

The transform step is covered by unit tests (type parsing, coordinate splitting, deduplication, tsunami flag). The dbt layer adds `not_null` tests on the silver source columns and `not_null` plus `unique` tests on the gold daily date. Event time is taken from the ISO `DateTime` field in UTC instead of the locale-formatted date and time strings, which avoids ambiguity from local month names and time zones.

**Design notes and limitations**

The BMKG endpoint only returns the most recent events, so a single run produces only a small number of rows. The dataset grows only when the extract step is run repeatedly. Deduplication in the silver layer is what makes repeated runs safe.

The API response format is not under my control, so the unit tests act as an early warning if the structure changes.

**Planned improvements**

Schedule the pipeline daily with Airflow, run pytest automatically with GitHub Actions, and swap the local folders for S3-compatible object storage (MinIO) to better mirror a real data lake.
