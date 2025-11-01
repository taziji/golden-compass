"""Utilities for fetching and caching datasets."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable

import pandas as pd

from golden_compass.config import get_settings
from golden_compass.data.sources import DataSource
from golden_compass.services import fred, twelve_data


LoaderOverrides = Dict[str, Dict[str, Any]]


def load_series(
    series: Iterable[DataSource], overrides: LoaderOverrides | None = None
) -> Dict[str, pd.DataFrame]:
    """Fetch a collection of series and return them keyed by identifier."""

    frames: Dict[str, pd.DataFrame] = {}
    for source in series:
        params = overrides.get(source.identifier, {}) if overrides else {}
        frames[source.identifier] = _load_single(source, params)
    return frames


def _load_single(source: DataSource, params: Dict[str, Any]) -> pd.DataFrame:
    """Load a single data source with caching."""

    cache_path = _cache_path(source)
    if cache_path.exists() and not params:
        return pd.read_parquet(cache_path)

    if source.loader == "fred":
        frame = fred.fetch_series(source.identifier, params=params)
    elif source.loader == "twelve_data":
        interval = params.pop("interval", "1h")
        frame = twelve_data.fetch_series(source.identifier, interval=interval, params=params)
    else:
        raise ValueError(f"Unsupported loader: {source.loader}")

    if not params:  # only cache canonical pulls to avoid fragmented cache files
        frame.to_parquet(cache_path)
        _write_metadata(cache_path.with_suffix(".json"), source)
    return frame


def _cache_path(source: DataSource) -> Path:
    settings = get_settings()
    sanitized = source.identifier.replace("/", "_").replace(" ", "_").lower()
    return settings.data_dir / f"{sanitized}.parquet"


def _write_metadata(path: Path, source: DataSource) -> None:
    metadata: Dict[str, Any] = {
        "name": source.name,
        "description": source.description,
        "identifier": source.identifier,
        "frequency": source.frequency,
        "loader": source.loader,
        "cached_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


__all__ = ["load_series"]
