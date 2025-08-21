class AppError(Exception):
    """Base class for all application errors."""

    pass


class CollectionNotFoundError(AppError):
    """Raised when a collection is not found."""

    pass
