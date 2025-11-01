"""Definitions for upstream data sources."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass(frozen=True)
class DataSource:
    """Metadata describing an upstream dataset."""

    name: str
    description: str
    loader: Literal["fred", "twelve_data", "local"]
    identifier: str
    frequency: Literal["intraday", "daily", "weekly", "monthly", "quarterly"]
    cn_description: Optional[str] = None
    notes: Optional[str] = None


FRED_SERIES = {
    "gvz": DataSource(
        name="CBOE Gold ETF Volatility Index",
        description="Volatility gauge for GLD options sourced via FRED (series GVZCLS).",
        cn_description=(
            "芝加哥期权交易所黄金波动率指数，用来衡量黄金期权隐含波动率，参考战术仓位的风险窗口。"
        ),
        loader="fred",
        identifier="GVZCLS",
        frequency="daily",
    ),
    "real_yield": DataSource(
        name="US 10Y Treasury Inflation-Indexed Security, Constant Maturity",
        description="Proxy for real yields; impacts gold opportunity cost.",
        cn_description=(
            "美国10年期通胀保值债券收益率，反映真实利率，用于判断黄金与无风险收益的相对吸引力。"
        ),
        loader="fred",
        identifier="DFII10",
        frequency="daily",
    ),
    "usd_liquidity": DataSource(
        name="Trade Weighted U.S. Dollar Index: Broad, Goods",
        description="Tracks broad USD strength as macro driver.",
        cn_description=(
            "贸易加权美元指数（商品篮子），观测美元流动性与外汇环境，对冲系统性美元走强风险。"
        ),
        loader="fred",
        identifier="DTWEXBGS",
        frequency="daily",
    ),
}

TWELVE_DATA_SERIES = {
    "xauusd_spot": DataSource(
        name="Spot Gold Price (XAU/USD)",
        description="Intraday price feed for gold spot.",
        cn_description="黄金现货价（美元计），提供日内价格行为用于战术信号确认。",
        loader="twelve_data",
        identifier="XAU/USD",
        frequency="intraday",
    ),
}

DEFAULT_SERIES = {
    **FRED_SERIES,
    **TWELVE_DATA_SERIES,
}

__all__ = [
    "DataSource",
    "FRED_SERIES",
    "TWELVE_DATA_SERIES",
    "DEFAULT_SERIES",
]
