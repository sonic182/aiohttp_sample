"""Logger middleware.

Adds logger adapter instance to request.
"""

from app.config.logger import MyLoggerAdapter


async def logger_middleware(app, handler):
    """Add uuid to request."""
    async def middleware_handler(request):
        """Handle middleware behaivor."""
        request.logger = MyLoggerAdapter(app.logger.logger, {
            'app': app, 'request': request})
        return await handler(request)
    return middleware_handler
