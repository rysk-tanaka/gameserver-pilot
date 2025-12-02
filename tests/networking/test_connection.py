"""Tests for the Connection class."""

from gameserver_pilot.networking.connection import Connection


def test_connection_creation() -> None:
    """Test creating a connection."""
    conn = Connection(id="conn-1")
    assert conn.id == "conn-1"
    assert conn.player_id is None
    assert not conn.is_authenticated


def test_connection_with_player() -> None:
    """Test connection with associated player."""
    conn = Connection(id="conn-1", player_id="player-1")
    assert conn.player_id == "player-1"
    assert conn.is_authenticated


def test_update_activity() -> None:
    """Test updating connection activity."""
    conn = Connection(id="conn-1")
    original_time = conn.last_activity

    conn.update_activity()

    assert conn.last_activity >= original_time
