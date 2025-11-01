"""Analytical helpers for trend and volatility studies."""
from __future__ import annotations

import pandas as pd


def compute_trend_channels(df: pd.DataFrame, price_col: str, window: int = 50) -> pd.DataFrame:
    """Calculate rolling mean and channel bounds."""

    if price_col not in df.columns:
        raise KeyError(f"Column '{price_col}' not present in DataFrame")

    result = df[["timestamp", price_col]].copy()
    result["ma"] = result[price_col].rolling(window=window, min_periods=1).mean()
    result["upper"] = result["ma"] * 1.03
    result["lower"] = result["ma"] * 0.97
    return result


def compute_volatility_bands(df: pd.DataFrame, price_col: str, window: int = 20) -> pd.DataFrame:
    """Compute rolling volatility metrics."""

    if price_col not in df.columns:
        raise KeyError(f"Column '{price_col}' not present in DataFrame")

    result = df[["timestamp", price_col]].copy()
    result["returns"] = result[price_col].pct_change()
    result["vol"] = result["returns"].rolling(window=window, min_periods=1).std() * (window ** 0.5)
    result["upper"] = result[price_col] * (1 + result["vol"])
    result["lower"] = result[price_col] * (1 - result["vol"])
    return result.drop(columns=["returns"])


__all__ = ["compute_trend_channels", "compute_volatility_bands"]
