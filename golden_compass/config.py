"""Configuration helpers for Golden Compass."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    environment: str = Field(default="local", description="Run environment identifier")
    data_dir: Path = Field(default=Path("data"), description="Path to local cache store")

    # API Keys
    fred_api_key: Optional[str] = Field(default=None, env="FRED_API_KEY")
    twelve_data_api_key: Optional[str] = Field(default=None, env="TWELVE_DATA_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""

    settings = Settings()
    settings.data_dir.mkdir(exist_ok=True, parents=True)
    return settings


__all__ = ["Settings", "get_settings"]
