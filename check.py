import duckdb

print(duckdb.sql("select * from 'data/gold/gempa_harian.parquet'"))