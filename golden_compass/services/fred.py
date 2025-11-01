"""Client utilities for the Federal Reserve Economic Data API."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import requests

from golden_compass.config import get_settings

FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_series(series_id: str, params: Dict[str, str] | None = None) -> pd.DataFrame:
    """Fetch a FRED time series and return a tidy DataFrame."""

    settings = get_settings()
    if not settings.fred_api_key:
        raise RuntimeError(
            "FRED API key is not configured. Set FRED_API_KEY in your environment."
        )

    query: Dict[str, str] = {
        "series_id": series_id,
        "api_key": settings.fred_api_key,
        "file_type": "json",
        "observation_start": "2010-01-01",
    }
    if params:
        query.update(params)

    response = requests.get(FRED_BASE_URL, params=query, timeout=30)
    response.raise_for_status()
    payload = response.json()
    observations = payload.get("observations", [])
    frame = pd.DataFrame(observations)
    if frame.empty:
        return frame

    frame["date"] = pd.to_datetime(frame["date"], format="%Y-%m-%d")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.rename(columns={"date": "timestamp", "value": series_id})
    frame = frame.drop(columns=[col for col in frame.columns if col not in {"timestamp", series_id}])
    frame = frame.dropna(subset=[series_id])
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    return frame


__all__ = ["fetch_series"]
