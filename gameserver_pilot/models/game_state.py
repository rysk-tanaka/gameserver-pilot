"""Game state model definition."""

from pydantic import BaseModel, Field

from gameserver_pilot.models.player import Player


class GameState(BaseModel):
    """Represents the current state of the game."""

    tick: int = Field(default=0, description="Current game tick")
    players: dict[str, Player] = Field(default_factory=dict, description="Connected players")
    started: bool = Field(default=False, description="Whether the game has started")

    def add_player(self, player: Player) -> None:
        """Add a player to the game state."""
        self.players[player.id] = player

    def remove_player(self, player_id: str) -> None:
        """Remove a player from the game state."""
        self.players.pop(player_id, None)

    def get_player(self, player_id: str) -> Player | None:
        """Get a player by ID."""
        return self.players.get(player_id)
