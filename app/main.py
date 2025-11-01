"""Main entry point for the Golden Compass Streamlit dashboard."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import streamlit as st

from golden_compass.analytics import compute_trend_channels, compute_volatility_bands
from golden_compass.config import get_settings
from golden_compass.data.loader import load_series
from golden_compass.data.sources import DEFAULT_SERIES, DataSource

st.set_page_config(page_title="Golden Compass", layout="wide", page_icon="🧭")

settings = get_settings()
ALL_SOURCES = list(DEFAULT_SERIES.values())
SOURCE_BY_IDENTIFIER = {source.identifier: source for source in ALL_SOURCES}


@st.cache_data(show_spinner=True)
def fetch_data(sources: list[DataSource], interval: str) -> Dict[str, pd.DataFrame]:
    """Fetch all configured datasets."""

    overrides: Dict[str, Dict[str, str]] = {}
    for source in sources:
        if source.loader == "twelve_data":
            overrides[source.identifier] = {"interval": interval}
    return load_series(sources, overrides=overrides)


st.title("Golden Compass Dashboard")
st.caption("Macro-guided gold monitoring")

with st.expander("指标说明 / Indicator Notes", expanded=False):
    for source in ALL_SOURCES:
        st.markdown(
            f"<strong>{source.name}</strong> — {source.description}<br/>"
            f"<code>{source.identifier}</code><br/>"
            f"{source.cn_description or ''}",
            unsafe_allow_html=True,
        )
        st.markdown("<hr>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Configuration")
    st.text(f"Environment: {settings.environment}")
    st.text(f"Cache: {settings.data_dir.resolve()}")
    selected_sources = st.multiselect(
        "Data sources",
        options=[source.name for source in ALL_SOURCES],
        default=[source.name for source in ALL_SOURCES],
    )

    interval = st.selectbox("Twelve Data interval", options=["15min", "1h", "4h", "1day"], index=1)

selected = [source for source in ALL_SOURCES if source.name in selected_sources]

if not selected:
    st.warning("Select at least one data source to visualize.")
    st.stop()

try:
    data_frames = fetch_data(selected, interval)
except RuntimeError as exc:
    st.error(f"Configuration issue: {exc}")
    st.info("Add API keys to .env and restart the app.")
    st.stop()
except Exception as exc:  # pragma: no cover - surfaced to user in UI
    st.error(f"Unexpected error: {exc}")
    st.stop()

st.success(f"Loaded {len(data_frames)} dataframes")

for identifier, frame in data_frames.items():
    source_meta = SOURCE_BY_IDENTIFIER.get(identifier)

    if frame.empty:
        st.warning(f"No data returned for {identifier}")
        continue

    display_name = source_meta.name if source_meta else identifier
    st.header(display_name)
    st.caption(identifier)
    if source_meta and source_meta.cn_description:
        st.markdown(source_meta.cn_description)

    st.dataframe(frame.tail(5), use_container_width=True)

    price_col = next((col for col in frame.columns if col != "timestamp"), None)
    if price_col is None:
        continue

    trend = compute_trend_channels(frame, price_col=price_col)
    volatility = compute_volatility_bands(frame, price_col=price_col)

    tabs = st.tabs(["Trend", "Volatility"])

    with tabs[0]:
        st.line_chart(
            trend.set_index("timestamp")[[price_col, "ma", "upper", "lower"]],
            use_container_width=True,
        )

    with tabs[1]:
        st.line_chart(
            volatility.set_index("timestamp")[[price_col, "upper", "lower"]],
            use_container_width=True,
        )

st.markdown("---")
st.caption(
    "Configure API keys via .env or environment variables (FRED_API_KEY, TWELVE_DATA_API_KEY)."
)
