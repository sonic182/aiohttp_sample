"""Json schema validator module."""

from json import loads
from json.decoder import JSONDecodeError

ERRORS = {
    '1': 'INVALID PAYLOAD',
    '2': 'INVALID DATA TYPE'
}


class JsonSchemaValidator:
    """Json Schema validator."""

    def __init__(self, constrain):
        """Set the constrain in object."""
        if not isinstance(constrain, dict):
            raise AttributeError('constrain must be a dict')
        self.constrain = constrain

    def validate(self, data, field='', constrain=None, started=False):
        """Validate incoming data."""
        res = {}
        errors = {}
        err = None

        if not started:
            constrain = self.constrain
            data, err = self._convert(data)
            started = True

        if constrain is None:
            return res, errors

        if err:
            return (False, {'payload': ERRORS[err]})

        my_field = field
        for key in constrain:
            field = my_field
            field += '.' if my_field else ''
            field += key

            if key not in data:
                errors[field] = 'Missing field'

            elif not isinstance(
                    data[key], constrain[key].get('type', str)):
                errors[field] = 'Bad data type'

            elif not self._extra_validations(data[key], constrain[key]):
                pass
            elif isinstance(data[key], dict):
                res2, errors2 = self.validate(
                    data[key], field, constrain[key].get('properties', None), started)

                if res2:
                    res[key] = res2

                if errors2:
                    errors[key] = errors2

            elif isinstance(data[key], list):
                res[key] = []

                my_field2 = field
                for ind, item in enumerate(data[key]):
                    field = my_field2
                    field += '.{}'.format(ind)
                    res2, errors2 = self.validate(
                        item, field, constrain[key], started)

                    if res2:
                        res[key].append(res2)

                    if errors2:
                        errors[key] = errors2
            else:
                res[key] = data[key]

        return res, errors

    @staticmethod
    def _extra_validations(data, constrain):
        """Extras validations."""
        return True

    @staticmethod
    def _convert(data):
        """Check if given data is a string, and loads it."""
        if JsonSchemaValidator._valid_data(data):
            if isinstance(data, str):
                try:
                    return (loads(data), False)
                except JSONDecodeError:
                    return (False, '1')
            else:
                return (data, False)
        return (False, '2')

    @staticmethod
    def _valid_data(data):
        choices = [str, dict, list]
        for _type in choices:
            if isinstance(data, _type):
                return True
        return False
