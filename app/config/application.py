"""Application module."""

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import SETTINGS

from app.controllers.users import map_users


async def startup(app):
    """Startup app."""
    # MONGO
    app.mongo_client = AsyncIOMotorClient(io_loop=app.loop)
    app.database = app.mongo_client[SETTINGS['mongo']['db']]


APP = web.Application()
APP.on_startup.append(startup)
map_users(APP)
