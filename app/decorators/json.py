"""Decorator for sonic182_json_validator."""
from json_validator.validator import JsonValidator
from aiohttp.web import json_response


class JsonValidate(object):
    """Validate incoming json."""

    def __init__(self, constrain):
        """Initializate object."""
        self.constrain = constrain

    def __call__(self, func):
        """Do json validation.

        If there is an error, the response will be 422 and the json error.
        """
        async def _wrapper(obj, req):
            res, err = JsonValidator(self.constrain).validate(
                await req.text())

            if err:
                return json_response(err, status=422)

            req.payload = res
            return await func(obj, req)
        return _wrapper
