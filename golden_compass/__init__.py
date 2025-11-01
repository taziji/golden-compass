"""Core package for Golden Compass dashboard."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("golden-compass")
except PackageNotFoundError:  # pragma: no cover - fallback when package not installed
    __version__ = "0.1.0"

__all__ = ["__version__"]
