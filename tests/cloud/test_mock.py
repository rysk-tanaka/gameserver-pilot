"""Tests for the mock cloud provider."""

import pytest

from gameserver_pilot.cloud.mock import MockProvider


@pytest.fixture
def provider() -> MockProvider:
    """Create a mock provider instance."""
    return MockProvider()


async def test_initial_status(provider: MockProvider) -> None:
    """Test that servers start in stopped state."""
    status = await provider.get_server_status("terraria")
    assert status == "stopped"


async def test_start_server(provider: MockProvider) -> None:
    """Test starting a server."""
    success = await provider.start_server("terraria")
    assert success is True

    status = await provider.get_server_status("terraria")
    assert status == "running"


async def test_stop_server(provider: MockProvider) -> None:
    """Test stopping a server."""
    await provider.start_server("terraria")
    success = await provider.stop_server("terraria")
    assert success is True

    status = await provider.get_server_status("terraria")
    assert status == "stopped"


async def test_get_ip_when_running(provider: MockProvider) -> None:
    """Test that IP is available when server is running."""
    await provider.start_server("terraria")
    ip = await provider.get_server_ip("terraria")
    assert ip is not None


async def test_get_ip_when_stopped(provider: MockProvider) -> None:
    """Test that IP is None when server is stopped."""
    ip = await provider.get_server_ip("terraria")
    assert ip is None


async def test_unknown_server(provider: MockProvider) -> None:
    """Test operations on unknown server."""
    status = await provider.get_server_status("unknown")
    assert status == "unknown"

    success = await provider.start_server("unknown")
    assert success is False
