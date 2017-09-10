"""Base class for models."""


class BaseModel(object):
    """Class base for database models."""

    def __init__(self, req):
        """Get collection instance from db."""
        self.collection = req.app.database[self.__class__.__name__.lower()]

    def __getattribute__(self, name):
        """Override get attribute."""
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return object.__getattribute__(self.collection, name)
