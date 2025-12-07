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

    # Beszel monitoring (optional)
    beszel_hub_url: str | None = None
    beszel_email: str | None = None
    beszel_password: str | None = None
    beszel_report_channel_id: int | None = None

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.env == "production"

    @property
    def beszel_configured(self) -> bool:
        """Check if Beszel monitoring is configured."""
        return bool(
            self.beszel_hub_url
            and self.beszel_email
            and self.beszel_password
            and self.beszel_report_channel_id
        )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
