"""Tests for the Player model."""

import pytest
from pydantic import ValidationError

from gameserver_pilot.models.player import Player


def test_player_creation() -> None:
    """Test creating a player with required fields."""
    player = Player(id="player-1", name="TestPlayer")
    assert player.id == "player-1"
    assert player.name == "TestPlayer"
    assert player.x == 0.0
    assert player.y == 0.0
    assert player.score == 0
    assert player.connected is True


def test_player_with_position() -> None:
    """Test creating a player with custom position."""
    player = Player(id="player-1", name="TestPlayer", x=10.5, y=20.3)
    assert player.x == 10.5
    assert player.y == 20.3


def test_player_requires_id() -> None:
    """Test that player requires an ID."""
    with pytest.raises(ValidationError):
        Player(name="TestPlayer")  # type: ignore[call-arg]


def test_player_requires_name() -> None:
    """Test that player requires a name."""
    with pytest.raises(ValidationError):
        Player(id="player-1")  # type: ignore[call-arg]
