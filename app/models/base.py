"""Base class for models."""


from json import dumps
from bson import json_util


class BaseModel(object):
    """Base for database models."""

    def __init__(self, app):
        """Get collection instance from db."""
        self.collection = app.database[self.__class__.__name__.lower()]

    def __getattribute__(self, name):
        """Override get attribute."""
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return object.__getattribute__(self.collection, name)

    @staticmethod
    def serialize(data):
        """Asdf."""
        for item in data:
            item['_id'] = str(item['_id'])
        return data
        # return dumps(data, default=json_util.default)
