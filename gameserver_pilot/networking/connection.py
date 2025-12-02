"""Connection handling for game clients."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Connection:
    """Represents a client connection to the game server."""

    id: str
    player_id: str | None = None
    connected_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)

    def update_activity(self) -> None:
        """Update the last activity timestamp."""
        self.last_activity = datetime.now()

    @property
    def is_authenticated(self) -> bool:
        """Check if the connection has an associated player."""
        return self.player_id is not None
