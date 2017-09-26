"""Controller base.

TODO: check if there is any usage for a base controller.
"""

from aiohttp.web import json_response


class Controller:
    """Controller base class."""

    @staticmethod
    def json_response(data, *args, **kwargs):
        """Response json wrapper, to do self.json_response."""
        return json_response(data, *args, **kwargs)

    @staticmethod
    async def write(req, response):
        """Send response.

        Usefull if you need to process something after response.
        """
        await response.prepare(req)
        await response.write_eof()
