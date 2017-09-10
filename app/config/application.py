"""Application module."""

from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import SETTINGS
from app.config.routes import map_routes


async def startup(app):
    """Startup app."""
    # MONGO
    app.mongo_client = AsyncIOMotorClient(io_loop=app.loop)
    app.database = app.mongo_client[SETTINGS['mongo']['db']]


def app_config(app):
    """Add app configs."""
    app.on_startup.append(startup)
    map_routes(app)
    return app
