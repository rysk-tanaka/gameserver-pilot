"""Mock cloud provider for development and testing."""

from gameserver_pilot.cloud.base import CloudProvider


class MockProvider(CloudProvider):
    """Mock implementation of CloudProvider for development."""

    def __init__(self) -> None:
        """Initialize mock provider with simulated server states."""
        self._servers: dict[str, dict[str, str | None]] = {
            "terraria": {"status": "stopped", "ip": None},
            "corekeeper": {"status": "stopped", "ip": None},
        }

    async def start_server(self, server_id: str) -> bool:
        """Simulate starting a server."""
        if server_id in self._servers:
            self._servers[server_id]["status"] = "running"
            self._servers[server_id]["ip"] = f"192.168.1.{hash(server_id) % 255}"
            return True
        return False

    async def stop_server(self, server_id: str) -> bool:
        """Simulate stopping a server."""
        if server_id in self._servers:
            self._servers[server_id]["status"] = "stopped"
            self._servers[server_id]["ip"] = None
            return True
        return False

    async def get_server_status(self, server_id: str) -> str:
        """Get simulated server status."""
        if server_id in self._servers:
            return str(self._servers[server_id]["status"])
        return "unknown"

    async def get_server_ip(self, server_id: str) -> str | None:
        """Get simulated server IP."""
        if server_id in self._servers:
            ip = self._servers[server_id]["ip"]
            return str(ip) if ip else None
        return None
