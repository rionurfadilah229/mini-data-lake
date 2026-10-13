import json
from datetime import datetime
from pathlib import Path

import requests

URL = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
BRONZE_DIR = Path("data/bronze")


def extract():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = BRONZE_DIR / f"gempa_{timestamp}.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    extract()