"""Main game server implementation."""

from gameserver_pilot.config import ServerConfig


class GameServer:
    """Main game server class that manages connections and game state."""

    def __init__(self, config: ServerConfig | None = None) -> None:
        """Initialize the game server.

        Args:
            config: Server configuration. Uses defaults if not provided.
        """
        self.config = config or ServerConfig()
        self._running = False

    def run(self) -> None:
        """Start the game server."""
        self._running = True
        print(f"Game server starting on port {self.config.port}...")

    def stop(self) -> None:
        """Stop the game server."""
        self._running = False
        print("Game server stopped.")

    @property
    def is_running(self) -> bool:
        """Check if the server is currently running."""
        return self._running
