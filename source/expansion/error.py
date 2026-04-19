class CacheError(Exception):
    """Raised when a cache operation fails."""

    def __init__(self, message: str):
        super().__init__(message)
