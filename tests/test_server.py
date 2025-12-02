"""Tests for the main game server."""

from gameserver_pilot import GameServer
from gameserver_pilot.config import ServerConfig


def test_server_initialization() -> None:
    """Test that the server initializes with default config."""
    server = GameServer()
    assert server.config is not None
    assert server.config.port == 8080
    assert not server.is_running


def test_server_with_custom_config() -> None:
    """Test server initialization with custom config."""
    config = ServerConfig(port=9000, max_players=50)
    server = GameServer(config=config)
    assert server.config.port == 9000
    assert server.config.max_players == 50


def test_server_running_state() -> None:
    """Test server running state changes."""
    server = GameServer()
    assert not server.is_running

    server.run()
    assert server.is_running

    server.stop()
    assert not server.is_running
