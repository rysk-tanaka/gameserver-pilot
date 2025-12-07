"""TShock REST API player monitor for Terraria servers."""

from http import HTTPStatus

import httpx

from gameserver_pilot.monitors.base import PlayerMonitor


class TShockMonitor(PlayerMonitor):
    """Player monitor using TShock REST API."""

    def __init__(self, host: str, port: int = 7878, token: str = "") -> None:
        """Initialize TShock monitor.

        Args:
            host: Server hostname or IP.
            port: REST API port (default: 7878).
            token: API authentication token.
        """
        self.base_url = f"http://{host}:{port}"
        self.token = token
        self.timeout = 10.0

    async def get_player_count(self) -> int:
        """Get player count from TShock REST API."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/v2/players/list",
                    params={"token": self.token},
                )
                response.raise_for_status()
                data = response.json()
                players = data.get("players", [])
                return len(players)
        except httpx.HTTPError:
            return 0

    async def is_available(self) -> bool:
        """Check if TShock REST API is reachable."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/v2/server/status")
                return response.status_code == HTTPStatus.OK
        except httpx.HTTPError:
            return False
