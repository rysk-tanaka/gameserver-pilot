"""Tests for application configuration."""

from gameserver_pilot.config import Settings

DEFAULT_AUTO_STOP_MINUTES = 60


def test_default_settings() -> None:
    """Test default configuration values."""
    settings = Settings()
    assert settings.env == "development"
    assert settings.auto_stop_minutes == DEFAULT_AUTO_STOP_MINUTES
    assert settings.aws_default_region == "ap-northeast-1"


def test_is_production_false() -> None:
    """Test is_production returns False for development."""
    settings = Settings(env="development")
    assert settings.is_production is False


def test_is_production_true() -> None:
    """Test is_production returns True for production."""
    settings = Settings(env="production")
    assert settings.is_production is True
