class AppError(Exception):
    """Base class for all application errors."""

    pass


class CollectionNotFoundError(AppError):
    """Raised when a collection is not found."""

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        super().__init__(f"Collection '{collection_name}' does not exist")
