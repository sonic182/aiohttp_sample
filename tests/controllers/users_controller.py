"""Users controller test."""

from aiohttp.web import Application
from app.config.application import app_config
from app.config.logger import LOGGER
from app.models.user import User


async def get_client_app(test_client):
    """Get client and app."""
    app = Application(logger=LOGGER)
    app_config(app)
    client = await test_client(app)
    return app, client


async def test_show_users(test_client):
    """Test show users."""
    app, client = await get_client_app(test_client)

    resp = await client.get(
        app.router['users'].url_for(_id='')
    )
    assert resp.status == 200

    users = await resp.json()
    my_users = await User(app).find({}).to_list(None)
    my_users = User.serialize(my_users)
    assert len(users) == len(my_users)


async def test_create_user(test_client):
    """Test create user."""
    app, client = await get_client_app(test_client)

    my_user = {'name': 'johanderson'}
    resp = await client.post(
        app.router['users'].url_for(_id=''),
        json=my_user
    )
    assert resp.status == 200

    user = await resp.json()
    assert '_id' in user
    assert user['name'] == my_user['name']
