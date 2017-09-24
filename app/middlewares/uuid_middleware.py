"""UUID middleware.

Adds unique identificator to request.
"""

from uuid import uuid1


async def uuid_middleware(app, handler):
    """Add uuid to request."""
    async def middleware_handler(request):
        """Handle middleware behaivor."""
        request.uuid = str(uuid1())
        return await handler(request)
    return middleware_handler
