"""Beszel API client for fetching server metrics."""

import httpx
from pydantic import BaseModel


class ServerMetrics(BaseModel):
    """Server metrics data from Beszel."""

    name: str
    status: str
    cpu: float
    memory: float
    disk: float


class BeszelClient:
    """Client for Beszel Hub REST API (PocketBase)."""

    def __init__(self, hub_url: str, email: str, password: str) -> None:
        """Initialize the Beszel client.

        Args:
            hub_url: Base URL of the Beszel Hub (e.g., https://beszel.railway.app)
            email: Admin email for authentication
            password: Admin password for authentication
        """
        self.hub_url = hub_url.rstrip("/")
        self.email = email
        self.password = password
        self._token: str | None = None

    async def _authenticate(self, client: httpx.AsyncClient) -> str:
        """Authenticate with Beszel Hub and return token.

        Args:
            client: HTTP client to use for the request

        Returns:
            Authentication token

        Raises:
            httpx.HTTPStatusError: If authentication fails
        """
        if self._token:
            return self._token

        try:
            response = await client.post(
                f"{self.hub_url}/api/collections/users/auth-with-password",
                json={"identity": self.email, "password": self.password},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            token: str = data["token"]
            self._token = token
            return token
        finally:
            self.password = ""  # Always clear password after auth attempt

    async def get_all_systems(self) -> list[ServerMetrics]:
        """Fetch metrics for all monitored systems.

        Returns:
            List of ServerMetrics for each system

        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        async with httpx.AsyncClient() as client:
            token = await self._authenticate(client)
            headers = {"Authorization": token}

            response = await client.get(
                f"{self.hub_url}/api/collections/systems/records",
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()

            return [
                ServerMetrics(
                    name=item["name"],
                    status=item.get("status", "unknown"),
                    cpu=item.get("info", {}).get("cpu", 0.0),
                    memory=item.get("info", {}).get("mem", 0.0),
                    disk=item.get("info", {}).get("disk", 0.0),
                )
                for item in data.get("items", [])
            ]

    def clear_token(self) -> None:
        """Clear cached authentication token."""
        self._token = None
