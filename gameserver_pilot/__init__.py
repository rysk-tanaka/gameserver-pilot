"""gameserver-pilot: A scalable game server framework for real-time multiplayer games."""

from gameserver_pilot.server import GameServer

__version__ = "0.1.0"
__all__ = ["GameServer", "main"]


def main() -> None:
    """Entry point for the gameserver-pilot CLI."""
    server = GameServer()
    server.run()
