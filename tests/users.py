"""Users controller test."""
from app.config.application import APP


async def test_create_user(test_client):
    """Test create user."""
    client = await test_client(APP)

    my_user = {'name': 'johanderson'}
    resp = await client.post('/users/', json=my_user)
    assert resp.status == 200

    user = await resp.json()
    assert '_id' in user
    assert user['name'] == my_user['name']
