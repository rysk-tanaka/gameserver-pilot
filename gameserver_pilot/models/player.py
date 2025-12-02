"""Player model definition."""

from pydantic import BaseModel, Field


class Player(BaseModel):
    """Represents a player in the game."""

    id: str = Field(..., description="Unique player identifier")
    name: str = Field(..., description="Player display name")
    x: float = Field(default=0.0, description="X position")
    y: float = Field(default=0.0, description="Y position")
    score: int = Field(default=0, description="Player score")
    connected: bool = Field(default=True, description="Connection status")
