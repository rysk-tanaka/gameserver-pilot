"""Application configuration management."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Discord
    discord_token: str = ""

    # AWS
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "ap-northeast-1"

    # Environment
    env: str = "development"

    # Auto-stop settings
    auto_stop_minutes: int = 60

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.env == "production"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
