"""UUID middleware.

Adds unique identificator to request.
"""

from uuid import uuid4


async def uuid_middleware(app, handler):
    """Add uuid to request."""
    async def middleware_handler(request):
        request.uuid = str(uuid4())
        return await handler(request)
    return middleware_handler
