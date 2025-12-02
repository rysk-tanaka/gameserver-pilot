"""Abstract base class for cloud providers."""

from abc import ABC, abstractmethod


class CloudProvider(ABC):
    """Abstract base class for cloud provider implementations."""

    @abstractmethod
    async def start_server(self, server_id: str) -> bool:
        """Start a server instance.

        Args:
            server_id: The server/instance identifier.

        Returns:
            True if the server was started successfully.
        """
        ...

    @abstractmethod
    async def stop_server(self, server_id: str) -> bool:
        """Stop a server instance.

        Args:
            server_id: The server/instance identifier.

        Returns:
            True if the server was stopped successfully.
        """
        ...

    @abstractmethod
    async def get_server_status(self, server_id: str) -> str:
        """Get the current status of a server.

        Args:
            server_id: The server/instance identifier.

        Returns:
            Status string (e.g., "running", "stopped", "pending").
        """
        ...

    @abstractmethod
    async def get_server_ip(self, server_id: str) -> str | None:
        """Get the public IP address of a server.

        Args:
            server_id: The server/instance identifier.

        Returns:
            Public IP address or None if not available.
        """
        ...
