"""Common functios for tests."""

from aiohttp.web import Application

from app.config.application import app_config
from app.config.logger import get_logger
from app.config.settings import basepath
from app.config.settings import SETTINGS

from app.middlewares import MIDDLEWARES


async def get_client_app(test_client):
    """Get client and app."""
    # Use other db for test
    SETTINGS['mongo']['db'] = 'aiohttp_test_db'

    app = Application(
        debug=True,
        logger=get_logger(logpath=basepath('logs', 'test.log'), debug=True),
        middlewares=MIDDLEWARES
    )
    app_config(app)

    client = await test_client(app)

    # drop old test db
    await app.mongo_client.drop_database(app.database)
    return app, client
