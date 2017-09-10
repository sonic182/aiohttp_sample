
from json import dumps

from aiohttp import web

from app.models.user import User


async def create(req):
    """Do test route."""
    data = await req.json()
    user = await User(req).insert_one(data)
    data['_id'] = str(user.inserted_id)
    return web.Response(text=dumps(data), content_type='application/json')


def map_users(app):
    """Map handlers to app."""
    app.router.add_post('/users/', create)
