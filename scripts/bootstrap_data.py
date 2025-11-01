"""Bootstrap script to warm cache with baseline datasets."""
from __future__ import annotations

from golden_compass.data.loader import load_series
from golden_compass.data.sources import DEFAULT_SERIES


def main() -> None:
    frames = load_series(DEFAULT_SERIES.values())
    print(f"Fetched {len(frames)} datasets")


if __name__ == "__main__":
    main()
