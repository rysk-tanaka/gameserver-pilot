"""Abstract base class for player monitors."""

from abc import ABC, abstractmethod


class PlayerMonitor(ABC):
    """Abstract base class for player monitoring implementations."""

    @abstractmethod
    async def get_player_count(self) -> int:
        """Get the current number of players on the server.

        Returns:
            Number of players currently connected.
        """
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the monitor can connect to the server.

        Returns:
            True if the server is reachable and monitoring is possible.
        """
        ...
