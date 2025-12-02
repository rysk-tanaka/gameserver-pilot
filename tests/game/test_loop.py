"""Tests for the GameLoop class."""

from gameserver_pilot.game.loop import GameLoop
from gameserver_pilot.models.game_state import GameState


def test_game_loop_initialization() -> None:
    """Test game loop initialization."""
    loop = GameLoop(tick_rate=60)
    assert loop.tick_rate == 60
    assert loop.tick_duration == 1.0 / 60


def test_register_callback() -> None:
    """Test registering a callback."""
    loop = GameLoop()
    called = []

    def callback(state: GameState) -> None:
        called.append(state.tick)

    loop.register_callback(callback)
    assert len(loop._callbacks) == 1


def test_game_loop_stop() -> None:
    """Test stopping the game loop."""
    loop = GameLoop()
    loop._running = True

    loop.stop()

    assert not loop._running
