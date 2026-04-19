__all__ = ["Account"]


class Account:
    """Represents a user account for XHS."""

    def __init__(self, user_id: str | None = None, name: str | None = None):
        self.user_id = user_id
        self.name = name
