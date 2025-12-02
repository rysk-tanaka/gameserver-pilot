"""Tests for the GameState model."""

from gameserver_pilot.models.game_state import GameState
from gameserver_pilot.models.player import Player


def test_game_state_initialization() -> None:
    """Test initial game state values."""
    state = GameState()
    assert state.tick == 0
    assert state.players == {}
    assert state.started is False


def test_add_player() -> None:
    """Test adding a player to the game state."""
    state = GameState()
    player = Player(id="player-1", name="TestPlayer")

    state.add_player(player)

    assert "player-1" in state.players
    assert state.players["player-1"].name == "TestPlayer"


def test_remove_player() -> None:
    """Test removing a player from the game state."""
    state = GameState()
    player = Player(id="player-1", name="TestPlayer")
    state.add_player(player)

    state.remove_player("player-1")

    assert "player-1" not in state.players


def test_remove_nonexistent_player() -> None:
    """Test removing a player that doesn't exist (should not raise)."""
    state = GameState()
    state.remove_player("nonexistent")  # Should not raise


def test_get_player() -> None:
    """Test getting a player by ID."""
    state = GameState()
    player = Player(id="player-1", name="TestPlayer")
    state.add_player(player)

    retrieved = state.get_player("player-1")
    assert retrieved is not None
    assert retrieved.name == "TestPlayer"


def test_get_nonexistent_player() -> None:
    """Test getting a player that doesn't exist."""
    state = GameState()
    assert state.get_player("nonexistent") is None
