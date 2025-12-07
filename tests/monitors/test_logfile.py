"""Tests for the log file player monitor."""

from pathlib import Path

import pytest

from gameserver_pilot.monitors.logfile import LogFileMonitor


@pytest.fixture
def temp_log(tmp_path: Path) -> Path:
    """Create a temporary log file."""
    log_file = tmp_path / "server.log"
    log_file.touch()
    return log_file


async def test_empty_log(temp_log: Path) -> None:
    """Test player count with empty log file."""
    monitor = LogFileMonitor(str(temp_log))
    count = await monitor.get_player_count()
    assert count == 0


async def test_player_join(temp_log: Path) -> None:
    """Test detecting player join."""
    temp_log.write_text("PlayerOne has joined\n")
    monitor = LogFileMonitor(str(temp_log))
    count = await monitor.get_player_count()
    assert count == 1


async def test_player_join_and_leave(temp_log: Path) -> None:
    """Test detecting player join and leave."""
    temp_log.write_text("PlayerOne has joined\nPlayerOne has left\n")
    monitor = LogFileMonitor(str(temp_log))
    count = await monitor.get_player_count()
    assert count == 0


async def test_multiple_players(temp_log: Path) -> None:
    """Test multiple players."""
    temp_log.write_text("PlayerOne has joined\nPlayerTwo has joined\nPlayerOne has left\n")
    monitor = LogFileMonitor(str(temp_log))
    count = await monitor.get_player_count()
    assert count == 1


async def test_is_available(temp_log: Path) -> None:
    """Test availability check."""
    monitor = LogFileMonitor(str(temp_log))
    assert await monitor.is_available() is True


async def test_not_available() -> None:
    """Test availability with missing file."""
    monitor = LogFileMonitor("/nonexistent/path/log.txt")
    assert await monitor.is_available() is False


async def test_custom_patterns(temp_log: Path) -> None:
    """Test custom join/leave patterns."""
    temp_log.write_text("User alice connected\nUser bob connected\nUser alice disconnected\n")
    monitor = LogFileMonitor(
        str(temp_log),
        join_pattern=r"User (.+) connected",
        leave_pattern=r"User (.+) disconnected",
    )
    count = await monitor.get_player_count()
    assert count == 1
