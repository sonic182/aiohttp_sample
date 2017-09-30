"""Test User model."""

from app.models.base import BaseModel
from tests.common import get_client_app


async def test_serialize(test_client):
    """Test serialize function of BaseModel."""
    app, client = await get_client_app(test_client)

    obj = {'foo': 'bar'}
    await BaseModel(app).insert_one(obj)
    items = await BaseModel(app).find({}).to_list(None)
    assert len(BaseModel.serialize(items)) is 1
