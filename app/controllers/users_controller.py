
from aiohttp.web import json_response

from app.controllers.base import Controller
from app.models.user import User


class UserController(Controller):

    async def index(self, req):
        """Index test route."""
        data = await User(req.app).find({}).to_list(None)
        return json_response(User.serialize(data))

    async def create(self, req):
        """Do test route."""
        data = await req.json()
        user = await User(req.app).insert_one(data)
        data['_id'] = str(user.inserted_id)
        return json_response(data)
