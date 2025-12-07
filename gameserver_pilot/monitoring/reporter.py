"""Periodic reporting of server metrics to Discord."""

import logging

import discord
from discord.ext import commands, tasks

from gameserver_pilot.monitoring.beszel_client import BeszelClient

logger = logging.getLogger(__name__)

REPORT_INTERVAL_HOURS = 24


class MonitoringReporter:
    """Sends periodic server monitoring reports to Discord."""

    def __init__(
        self,
        bot: commands.Bot,
        beszel: BeszelClient,
        channel_id: int,
    ) -> None:
        """Initialize the monitoring reporter.

        Args:
            bot: Discord bot instance
            beszel: Beszel API client
            channel_id: Discord channel ID for reports
        """
        self.bot = bot
        self.beszel = beszel
        self.channel_id = channel_id

    @tasks.loop(hours=REPORT_INTERVAL_HOURS)
    async def daily_report(self) -> None:
        """Send daily server status report."""
        channel = self.bot.get_channel(self.channel_id)
        if not channel or not isinstance(channel, discord.TextChannel):
            logger.warning("Report channel not found: %s", self.channel_id)
            return

        try:
            systems = await self.beszel.get_all_systems()
        except Exception:
            logger.exception("Failed to fetch systems from Beszel")
            return

        if not systems:
            logger.info("No systems to report")
            return

        embed = discord.Embed(
            title="Daily Server Report",
            color=discord.Color.blue(),
        )

        for sys in systems:
            status_indicator = "+" if sys.status == "up" else "-"
            embed.add_field(
                name=f"{status_indicator} {sys.name}",
                value=f"CPU: {sys.cpu:.1f}%\nRAM: {sys.memory:.1f}%\nDisk: {sys.disk:.1f}%",
                inline=True,
            )

        await channel.send(embed=embed)
        logger.info("Daily report sent to channel %s", self.channel_id)

    @daily_report.before_loop
    async def before_daily_report(self) -> None:
        """Wait for bot to be ready before starting the loop."""
        await self.bot.wait_until_ready()

    def start(self) -> None:
        """Start the daily report task."""
        self.daily_report.start()

    def stop(self) -> None:
        """Stop the daily report task."""
        self.daily_report.cancel()
