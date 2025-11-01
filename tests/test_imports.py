"""Basic smoke tests for package imports."""
from golden_compass import __version__


def test_version() -> None:
    assert __version__ == "0.1.0"
