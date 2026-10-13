import json
from pathlib import Path

import pandas as pd

BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver")


def load_bronze() -> pd.DataFrame:
    rows = []
    for f in sorted(BRONZE_DIR.glob("gempa_*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        rows.extend(data["Infogempa"]["gempa"])
    return pd.DataFrame(rows)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    coords = df["Coordinates"].str.split(",", expand=True).astype(float)

    out = pd.DataFrame()
    out["event_time_utc"] = pd.to_datetime(df["DateTime"], utc=True)
    out["latitude"] = coords[0]
    out["longitude"] = coords[1]
    out["magnitude"] = df["Magnitude"].astype(float)
    out["depth_km"] = df["Kedalaman"].str.extract(r"([\d.]+)")[0].astype(float)
    out["region"] = df["Wilayah"]
    out["tsunami_potential"] = ~df["Potensi"].str.startswith("Tidak")

    # data yang sama bisa muncul di banyak file bronze, jadi buang duplikat
    out = out.drop_duplicates(subset=["event_time_utc", "latitude", "longitude"])
    return out.sort_values("event_time_utc", ascending=False)


def main():
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    df = transform(load_bronze())
    out_path = SILVER_DIR / "gempa.parquet"
    df.to_parquet(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()