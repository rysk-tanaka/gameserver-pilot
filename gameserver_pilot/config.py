"""Server configuration management."""

from pydantic_settings import BaseSettings


class ServerConfig(BaseSettings):
    """Configuration for the game server."""

    host: str = "0.0.0.0"
    port: int = 8080
    tick_rate: int = 60
    max_players: int = 100
    log_level: str = "info"

    model_config = {"env_prefix": "GAMESERVER_"}
