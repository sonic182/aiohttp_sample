"""Sample UserController.

Minimal endpoint for users.
"""

from app.decorators.json import JsonValidate
from app.controllers.base import Controller
from app.models.user import User

CONSTRAIN = {
    'name': {
        'format': r'^[\w\s]+$'
    }
}


class UserController(Controller):
    """User controller."""

    async def index(self, req):
        """Index test route."""
        req.logger.info('mongo_request', data={
            'type': 'find',
            'query': {}
        })
        data = await User(req.app).find({}).to_list(None)
        data = User.serialize(data)
        req.logger.info('mongo_response', data={'response': data})
        return self.json_response(data)

    @JsonValidate(CONSTRAIN)
    async def create(self, req):
        """Do test route."""
        data = req.payload
        req.logger.info('mongo_request', data={
            'type': 'insert',
            'data': data,
        })
        user = await User(req.app).insert_one(data)
        data['_id'] = str(user.inserted_id)
        req.logger.info('mongo_response', data=data)
        await self.write(req, self.json_response(data))
        print('can continue doing stuff...')
