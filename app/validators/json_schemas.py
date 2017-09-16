"""Json schema validator module."""

from re import match
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
            return (None, {'payload': ERRORS[err]})

        my_field = field
        for key in constrain:
            field = my_field
            field += '.' if my_field else ''
            field += key

            if key not in data:
                if constrain[key].get('default', False):
                    res[key] = constrain[key]['default']

                else:
                    errors[field] = 'Missing field'
            else:
                self._key_match(data[key], constrain[key], key, field, started,
                                res, errors)

        return res, errors

    def _key_match(self, obj, rules, key, field, started, res, errors):
        """Extras validations."""
        if not isinstance(
                obj, rules.get('type', str)):
            errors[field] = 'Bad data type'

        elif not JsonSchemaValidator._extra_validations(
                obj, rules, errors, field):
            pass

        elif isinstance(obj, dict):
            res2, errors2 = self.validate(
                obj, field, rules.get(
                    'properties', None), started)

            res[key] = res2 or {}

            if errors2:
                errors[key] = errors2

        elif isinstance(obj, list):
            res[key] = []
            my_field2 = field
            for ind, item in enumerate(obj):
                field = my_field2
                field += '.{}'.format(ind)
                res[key].append(None)

                res2, errors2 = self._key_match(item, rules.get(
                    'items', {}), ind, field, started, res[key], {})

                if res2:
                    res[key] = res2
                res[key] = [x for x in res[key] if x is not None]

                if errors2:
                    if errors.get(key, None) is None:
                        errors[key] = []
                    errors[key].append(
                        errors2.get(ind, '') or errors2.get(field, ''))
        else:
            res[key] = obj

        return res, errors

    @staticmethod
    def _extra_validations(data, rules, errors, field):
        """Extras validations."""
        if isinstance(data, (int, float)):
            if rules.get('gt', False) and not data > rules['gt']:
                errors[field] = 'Not greater than %i' % rules['gt']
                return False

            elif rules.get('lt', False) and not data < rules['lt']:
                errors[field] = 'Not less than %i' % rules['lt']
                return False

        if rules.get('format', False):
            if not match(rules['format'], data):
                errors[field] = 'Invalid format'
                return False

        if rules.get('in', False):
            if data not in rules['in']:
                errors[field] = 'Invalid'
                return False

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
