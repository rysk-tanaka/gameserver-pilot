"""Discord bot for managing game servers."""

import discord
from discord import app_commands
from discord.ext import commands

from gameserver_pilot.cloud.base import CloudProvider
from gameserver_pilot.cloud.ec2 import EC2Provider
from gameserver_pilot.cloud.mock import MockProvider
from gameserver_pilot.config import settings
from gameserver_pilot.monitoring import BeszelClient, MonitoringReporter


class GameServerBot(commands.Bot):
    """Discord bot for game server management."""

    def __init__(self) -> None:
        """Initialize the bot."""
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

        # Use mock provider in development, EC2 in production
        self.cloud: CloudProvider
        if settings.is_production:
            self.cloud = EC2Provider(region=settings.aws_default_region)
        else:
            self.cloud = MockProvider()

        # Server ID mapping (server name -> instance ID)
        self.servers: dict[str, str] = {}

        # Monitoring reporter (optional)
        self.reporter: MonitoringReporter | None = None
        if settings.beszel_configured:
            assert settings.beszel_hub_url is not None
            assert settings.beszel_email is not None
            assert settings.beszel_password is not None
            assert settings.beszel_report_channel_id is not None
            beszel = BeszelClient(
                hub_url=settings.beszel_hub_url,
                email=settings.beszel_email,
                password=settings.beszel_password,
            )
            self.reporter = MonitoringReporter(
                bot=self,
                beszel=beszel,
                channel_id=settings.beszel_report_channel_id,
            )

    async def setup_hook(self) -> None:
        """Set up the bot before connecting."""
        self.tree.add_command(start_command)
        self.tree.add_command(stop_command)
        self.tree.add_command(status_command)
        await self.tree.sync()

    async def on_ready(self) -> None:
        """Handle bot ready event."""
        print(f"Logged in as {self.user}")
        print(f"Mode: {'production' if settings.is_production else 'development'}")

        # Start monitoring reporter if configured
        if self.reporter:
            self.reporter.start()
            print("Monitoring reporter started")


bot = GameServerBot()


@app_commands.command(name="start", description="Start a game server")
@app_commands.describe(server="The server to start")
async def start_command(interaction: discord.Interaction, server: str) -> None:
    """Start a game server."""
    await interaction.response.defer()

    server_id = bot.servers.get(server, server)
    success = await bot.cloud.start_server(server_id)

    if success:
        await interaction.followup.send(f"Starting server: {server}")
    else:
        await interaction.followup.send(f"Failed to start server: {server}")


@app_commands.command(name="stop", description="Stop a game server")
@app_commands.describe(server="The server to stop")
async def stop_command(interaction: discord.Interaction, server: str) -> None:
    """Stop a game server."""
    await interaction.response.defer()

    server_id = bot.servers.get(server, server)
    success = await bot.cloud.stop_server(server_id)

    if success:
        await interaction.followup.send(f"Stopping server: {server}")
    else:
        await interaction.followup.send(f"Failed to stop server: {server}")


@app_commands.command(name="status", description="Check game server status")
@app_commands.describe(server="The server to check")
async def status_command(interaction: discord.Interaction, server: str) -> None:
    """Check game server status."""
    await interaction.response.defer()

    server_id = bot.servers.get(server, server)
    status = await bot.cloud.get_server_status(server_id)
    ip = await bot.cloud.get_server_ip(server_id)

    message = f"**{server}**\nStatus: {status}"
    if ip:
        message += f"\nIP: {ip}"

    await interaction.followup.send(message)


def main() -> None:
    """Run the Discord bot."""
    if not settings.discord_token:
        print("Error: DISCORD_TOKEN environment variable is required")
        return

    bot.run(settings.discord_token)


if __name__ == "__main__":
    main()
