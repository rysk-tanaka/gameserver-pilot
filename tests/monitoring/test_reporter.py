"""Tests for the monitoring reporter."""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest

from gameserver_pilot.monitoring.beszel_client import BeszelClient, ServerMetrics
from gameserver_pilot.monitoring.reporter import MonitoringReporter

TEST_CHANNEL_ID = 123456789
EXPECTED_FIELD_COUNT = 2


@pytest.fixture
def mock_bot() -> MagicMock:
    """Create a mock Discord bot."""
    bot = MagicMock()
    bot.wait_until_ready = AsyncMock()
    return bot


@pytest.fixture
def mock_beszel() -> MagicMock:
    """Create a mock Beszel client."""
    return MagicMock(spec=BeszelClient)


@pytest.fixture
def reporter(mock_bot: MagicMock, mock_beszel: MagicMock) -> MonitoringReporter:
    """Create a reporter instance."""
    return MonitoringReporter(
        bot=mock_bot,
        beszel=mock_beszel,
        channel_id=TEST_CHANNEL_ID,
    )


async def test_daily_report_sends_embed(
    reporter: MonitoringReporter, mock_bot: MagicMock, mock_beszel: MagicMock
) -> None:
    """Test that daily report sends embed to channel."""
    mock_channel = MagicMock(spec=discord.TextChannel)
    mock_channel.send = AsyncMock()
    mock_bot.get_channel.return_value = mock_channel

    mock_beszel.get_all_systems = AsyncMock(
        return_value=[
            ServerMetrics(name="server1", status="up", cpu=50.0, memory=60.0, disk=30.0),
            ServerMetrics(name="server2", status="down", cpu=0.0, memory=0.0, disk=25.0),
        ]
    )

    await reporter.daily_report()

    mock_bot.get_channel.assert_called_once_with(TEST_CHANNEL_ID)
    mock_channel.send.assert_called_once()

    call_kwargs = mock_channel.send.call_args.kwargs
    embed = call_kwargs["embed"]
    assert embed.title == "Daily Server Report"
    assert len(embed.fields) == EXPECTED_FIELD_COUNT


async def test_daily_report_channel_not_found(
    reporter: MonitoringReporter, mock_bot: MagicMock
) -> None:
    """Test that report is skipped when channel not found."""
    mock_bot.get_channel.return_value = None

    with patch("gameserver_pilot.monitoring.reporter.logger") as mock_logger:
        await reporter.daily_report()
        mock_logger.warning.assert_called_once()


async def test_daily_report_api_error(
    reporter: MonitoringReporter, mock_bot: MagicMock, mock_beszel: MagicMock
) -> None:
    """Test that API errors are logged."""
    mock_channel = MagicMock(spec=discord.TextChannel)
    mock_bot.get_channel.return_value = mock_channel

    mock_beszel.get_all_systems = AsyncMock(side_effect=Exception("API Error"))

    with patch("gameserver_pilot.monitoring.reporter.logger") as mock_logger:
        await reporter.daily_report()
        mock_logger.exception.assert_called_once()


async def test_daily_report_no_systems(
    reporter: MonitoringReporter, mock_bot: MagicMock, mock_beszel: MagicMock
) -> None:
    """Test that empty system list is handled."""
    mock_channel = MagicMock(spec=discord.TextChannel)
    mock_bot.get_channel.return_value = mock_channel

    mock_beszel.get_all_systems = AsyncMock(return_value=[])

    with patch("gameserver_pilot.monitoring.reporter.logger") as mock_logger:
        await reporter.daily_report()
        mock_logger.info.assert_called_once()
        mock_channel.send.assert_not_called()


def test_start_begins_task(reporter: MonitoringReporter) -> None:
    """Test that start begins the daily report task."""
    with patch.object(reporter.daily_report, "start") as mock_start:
        reporter.start()
        mock_start.assert_called_once()


def test_stop_cancels_task(reporter: MonitoringReporter) -> None:
    """Test that stop cancels the daily report task."""
    with patch.object(reporter.daily_report, "cancel") as mock_cancel:
        reporter.stop()
        mock_cancel.assert_called_once()
