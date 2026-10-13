import pandas as pd

from src.transform import transform


def sample_row(**overrides):
    row = {
        "Tanggal": "12 Okt 2026",
        "Jam": "04:34:53 WIB",
        "DateTime": "2026-10-11T21:34:53+00:00",
        "Coordinates": "0.64,121.75",
        "Lintang": "0.64 LU",
        "Bujur": "121.75 BT",
        "Magnitude": "5.7",
        "Kedalaman": "76 km",
        "Wilayah": "29 km BaratLaut POHUWATO-GORONTALO",
        "Potensi": "Tidak berpotensi tsunami",
    }
    row.update(overrides)
    return row


def test_parsing_angka_dan_koordinat():
    out = transform(pd.DataFrame([sample_row()]))
    assert out["magnitude"].iloc[0] == 5.7
    assert out["depth_km"].iloc[0] == 76.0
    assert out["latitude"].iloc[0] == 0.64
    assert out["longitude"].iloc[0] == 121.75


def test_duplikat_dibuang():
    out = transform(pd.DataFrame([sample_row(), sample_row()]))
    assert len(out) == 1


def test_flag_tsunami():
    df = pd.DataFrame([sample_row(Potensi="Berpotensi tsunami")])
    assert transform(df)["tsunami_potential"].iloc[0]