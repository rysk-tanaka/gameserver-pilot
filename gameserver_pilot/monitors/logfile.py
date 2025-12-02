"""Log file based player monitor for various game servers."""

import re
from pathlib import Path

from gameserver_pilot.monitors.base import PlayerMonitor


class LogFileMonitor(PlayerMonitor):
    """Player monitor that parses game server log files."""

    def __init__(
        self,
        log_path: str,
        join_pattern: str = r"(.+) has joined",
        leave_pattern: str = r"(.+) has left",
    ) -> None:
        """Initialize log file monitor.

        Args:
            log_path: Path to the game server log file.
            join_pattern: Regex pattern for player join messages.
            leave_pattern: Regex pattern for player leave messages.
        """
        self.log_path = Path(log_path)
        self.join_regex = re.compile(join_pattern)
        self.leave_regex = re.compile(leave_pattern)

    async def get_player_count(self) -> int:
        """Parse log file to determine current player count."""
        if not self.log_path.exists():
            return 0

        players: set[str] = set()

        try:
            with self.log_path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    join_match = self.join_regex.search(line)
                    if join_match:
                        players.add(join_match.group(1))
                        continue

                    leave_match = self.leave_regex.search(line)
                    if leave_match:
                        players.discard(leave_match.group(1))
        except OSError:
            return 0

        return len(players)

    async def is_available(self) -> bool:
        """Check if log file exists and is readable."""
        return self.log_path.exists() and self.log_path.is_file()
