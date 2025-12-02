"""Game loop implementation."""

import time
from typing import Callable

from gameserver_pilot.models.game_state import GameState


class GameLoop:
    """Manages the game loop at a fixed tick rate."""

    def __init__(self, tick_rate: int = 60) -> None:
        """Initialize the game loop.

        Args:
            tick_rate: Number of ticks per second.
        """
        self.tick_rate = tick_rate
        self.tick_duration = 1.0 / tick_rate
        self._running = False
        self._callbacks: list[Callable[[GameState], None]] = []

    def register_callback(self, callback: Callable[[GameState], None]) -> None:
        """Register a callback to be called each tick."""
        self._callbacks.append(callback)

    def start(self, state: GameState) -> None:
        """Start the game loop."""
        self._running = True
        last_time = time.time()

        while self._running:
            current_time = time.time()
            elapsed = current_time - last_time

            if elapsed >= self.tick_duration:
                state.tick += 1
                for callback in self._callbacks:
                    callback(state)
                last_time = current_time
            else:
                time.sleep(self.tick_duration - elapsed)

    def stop(self) -> None:
        """Stop the game loop."""
        self._running = False
