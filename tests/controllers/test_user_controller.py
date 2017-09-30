"""Users controller test."""

from app.models.user import User
from tests.common import get_client_app


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


async def test_reject_request(test_client):
    """Test reject request."""
    app, client = await get_client_app(test_client)

    my_user = {'lastname': 'johanderson'}
    resp = await client.post(
        app.router['users'].url_for(_id=''),
        json=my_user
    )
    assert resp.status == 422
    assert (await resp.json()) == {'name': 'Missing field'}

    my_user = {'name': 'johanderson'}
    resp = await client.post(
        app.router['users'].url_for(_id=''),
        json=my_user
    )
    assert resp.status == 200

    user = await resp.json()
    assert '_id' in user
    assert user['name'] == my_user['name']
