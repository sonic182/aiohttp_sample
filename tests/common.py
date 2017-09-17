"""Common functios for tests."""

from aiohttp.web import Application

from app.config.application import app_config
from app.config.logger import get_logger
from app.config.settings import basepath
from app.config.settings import SETTINGS
from app.config.settings import load_environment

from app.middlewares import MIDDLEWARES

load_environment('test')


async def get_client_app(test_client):
    """Get client and app."""
    # Use other db for test
    SETTINGS['mongo']['db'] = 'aiohttp_test_db'

    logger = get_logger(
        debug=True,
        logpath=basepath('logs', 'test.log'),
    )

    app = Application(
        debug=True,
        logger=logger,
        middlewares=MIDDLEWARES
    )
    app_config(app)

    client = await test_client(app)

    # drop old test db
    await app.mongo_client.drop_database(app.database)
    return app, client
