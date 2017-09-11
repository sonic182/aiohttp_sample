"""Middlewares array."""

from app.middlewares.logger_middleware import logger_middleware
from app.middlewares.uuid_middleware import uuid_middleware


MIDDLEWARES = [
    logger_middleware,
    uuid_middleware,
]
