"""Client utilities for the Twelve Data market data API."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import requests

from golden_compass.config import get_settings

TWELVE_DATA_URL = "https://api.twelvedata.com/time_series"


def fetch_series(symbol: str, interval: str = "1h", params: Dict[str, str] | None = None) -> pd.DataFrame:
    """Fetch intraday series from Twelve Data."""

    settings = get_settings()
    if not settings.twelve_data_api_key:
        raise RuntimeError(
            "Twelve Data API key is not configured. Set TWELVE_DATA_API_KEY in your environment."
        )

    query: Dict[str, str] = {
        "symbol": symbol,
        "interval": interval,
        "apikey": settings.twelve_data_api_key,
        "format": "JSON",
        "outputsize": "5000",
    }
    if params:
        query.update(params)

    response = requests.get(TWELVE_DATA_URL, params=query, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if "values" not in payload:
        raise RuntimeError(f"Unexpected response from Twelve Data: {payload}")

    frame = pd.DataFrame(payload["values"])
    frame["datetime"] = pd.to_datetime(frame["datetime"])
    value_cols = [col for col in frame.columns if col != "datetime"]
    for col in value_cols:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.rename(columns={"datetime": "timestamp"})
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    return frame


__all__ = ["fetch_series"]
