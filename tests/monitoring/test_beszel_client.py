"""Tests for the Beszel API client."""

import httpx
import pytest
import respx

from gameserver_pilot.monitoring.beszel_client import BeszelClient, ServerMetrics

HUB_URL = "https://beszel.example.com"
TEST_EMAIL = "admin@example.com"
TEST_PASSWORD = "password123"
TEST_TOKEN = "test-auth-token"
EXPECTED_SYSTEM_COUNT = 2


@pytest.fixture
def client() -> BeszelClient:
    """Create a test Beszel client."""
    return BeszelClient(hub_url=HUB_URL, email=TEST_EMAIL, password=TEST_PASSWORD)


@respx.mock
async def test_authenticate_success(client: BeszelClient) -> None:
    """Test successful authentication."""
    respx.post(f"{HUB_URL}/api/collections/users/auth-with-password").mock(
        return_value=httpx.Response(200, json={"token": TEST_TOKEN})
    )

    async with httpx.AsyncClient() as http_client:
        token = await client._authenticate(http_client)

    assert token == TEST_TOKEN
    assert client._token == TEST_TOKEN


@respx.mock
async def test_authenticate_failure(client: BeszelClient) -> None:
    """Test authentication failure."""
    respx.post(f"{HUB_URL}/api/collections/users/auth-with-password").mock(
        return_value=httpx.Response(401, json={"message": "Invalid credentials"})
    )

    async with httpx.AsyncClient() as http_client:
        with pytest.raises(httpx.HTTPStatusError):
            await client._authenticate(http_client)


@respx.mock
async def test_authenticate_cached_token(client: BeszelClient) -> None:
    """Test that cached token is reused."""
    client._token = TEST_TOKEN

    async with httpx.AsyncClient() as http_client:
        token = await client._authenticate(http_client)

    assert token == TEST_TOKEN


@respx.mock
async def test_get_all_systems(client: BeszelClient) -> None:
    """Test fetching all monitored systems."""
    respx.post(f"{HUB_URL}/api/collections/users/auth-with-password").mock(
        return_value=httpx.Response(200, json={"token": TEST_TOKEN})
    )
    respx.get(f"{HUB_URL}/api/collections/systems/records").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [
                    {
                        "name": "terraria",
                        "status": "up",
                        "info": {"cpu": 25.5, "mem": 60.0, "disk": 40.0},
                    },
                    {
                        "name": "minecraft",
                        "status": "down",
                        "info": {"cpu": 0.0, "mem": 0.0, "disk": 35.0},
                    },
                ]
            },
        )
    )

    systems = await client.get_all_systems()

    assert len(systems) == EXPECTED_SYSTEM_COUNT
    assert systems[0] == ServerMetrics(
        name="terraria", status="up", cpu=25.5, memory=60.0, disk=40.0
    )
    assert systems[1] == ServerMetrics(
        name="minecraft", status="down", cpu=0.0, memory=0.0, disk=35.0
    )


@respx.mock
async def test_get_all_systems_empty(client: BeszelClient) -> None:
    """Test fetching systems when none are registered."""
    respx.post(f"{HUB_URL}/api/collections/users/auth-with-password").mock(
        return_value=httpx.Response(200, json={"token": TEST_TOKEN})
    )
    respx.get(f"{HUB_URL}/api/collections/systems/records").mock(
        return_value=httpx.Response(200, json={"items": []})
    )

    systems = await client.get_all_systems()

    assert systems == []


@respx.mock
async def test_get_all_systems_missing_info(client: BeszelClient) -> None:
    """Test handling systems with missing info fields."""
    respx.post(f"{HUB_URL}/api/collections/users/auth-with-password").mock(
        return_value=httpx.Response(200, json={"token": TEST_TOKEN})
    )
    respx.get(f"{HUB_URL}/api/collections/systems/records").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [
                    {"name": "server1", "status": "up"},
                ]
            },
        )
    )

    systems = await client.get_all_systems()

    assert len(systems) == 1
    assert systems[0].cpu == 0.0
    assert systems[0].memory == 0.0
    assert systems[0].disk == 0.0


def test_clear_token(client: BeszelClient) -> None:
    """Test clearing cached token."""
    client._token = TEST_TOKEN
    client.clear_token()
    assert client._token is None


def test_hub_url_trailing_slash() -> None:
    """Test that trailing slash is removed from hub URL."""
    client = BeszelClient(hub_url="https://example.com/", email=TEST_EMAIL, password=TEST_PASSWORD)
    assert client.hub_url == "https://example.com"
