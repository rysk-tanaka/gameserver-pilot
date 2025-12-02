"""ID generation utilities."""

import uuid


def generate_id() -> str:
    """Generate a unique ID for game entities."""
    return str(uuid.uuid4())
