class GTDError(Exception):
    """Base exception for GTD CLI errors."""
    pass

class ValidationError(GTDError):
    """Raised when input validation fails."""
    pass

class DatabaseError(GTDError):
    """Raised when database operations fail."""
    pass
