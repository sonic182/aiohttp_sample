"""Routes module."""
from app.controllers.users_controller import UserController


def map_routes(app):
    """Map routes to app object."""
    controller = UserController()
    resource = app.router.add_resource(r'/users/{_id:\d*}', name='users')
    resource.add_route('GET', controller.index)
    resource.add_route('POST', controller.create)
