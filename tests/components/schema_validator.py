"""Json schemas validator."""

from json import dumps
from json import loads
from datetime import datetime
from app.validators.json_schemas import JsonSchemaValidator


def test_validator_needs_constrain():
    """Test validator needs constrain."""
    try:
        JsonSchemaValidator('')
        assert False
    except AttributeError:
        assert True

    JsonSchemaValidator({})
    assert True


def test_validator_data_type():
    """Test validator recieves correct data type."""
    valid_objects = [{}, 'foo', []]
    for obj in valid_objects:
        assert JsonSchemaValidator._valid_data(obj)

    not_valid_objects = [1234, 1.2, False]
    for obj in not_valid_objects:
        assert JsonSchemaValidator._valid_data(obj) is False


def test_validator_valid_json():
    """Test validator recieves a valid json."""
    json_str = "{'foo': 'bar'}"
    res, err = JsonSchemaValidator._convert(json_str)
    assert err

    json_str = dumps({'foo': 'bar'})
    res, err = JsonSchemaValidator._convert(json_str)
    assert res


def test_constrain_primitive():
    """Test constrain primitive types"""
    constrain = {
        'string': {},
        'integer': {'type': int},
        'float': {'type': float},
        'boolean': {'type': bool},
        'json': {
            'type': dict
        },
        'list': {
            'type': list,
        },
        'extra_1': {},
        'extra_2': {},
    }
    json = dumps({
        'string': 'foo',
        'integer': 42,
        'float': 1.10,
        'boolean': True,
        'json': {},
        'list': []
    })

    res, err = JsonSchemaValidator(constrain).validate('{as: "df"}')
    assert err == {'payload': 'INVALID PAYLOAD'}

    res, err = JsonSchemaValidator(constrain).validate(json)
    assert err == {'extra_1': 'Missing field', 'extra_2': 'Missing field'}
    del constrain['extra_1']
    del constrain['extra_2']

    constrain['integer']['type'] = str
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert err == {'integer': 'Bad data type'}

    constrain['integer']['type'] = int
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res == loads(json)


def test_constrain_lists_dicts():
    """Test nested structures."""
    constrain = {
        'json': {
            'type': dict,
            'properties': {
                'integer': {'type': int},
                'float': {'type': float},
            }
        },
        'list': {
            'type': list,
            'items': {
                'type': dict,
                'properties': {
                    'name': {},
                    'lastname': {},
                    'age': {
                        'type': list,
                        'items': {
                            'type': int
                        }
                    }
                }
            }
        },
    }
    json = dumps({
        'json': {
            'integer': 42,
            'float': 12.12
        },
        'list': [{
            'name': 'johan',
            'lastname': 'mogollon',
        }, {
            'name': 'johan',
            'lastname': 'mogollon',
        }, {
            'name': 'jean',
            'lastname': 'paul',
            'age': [12, 24]
        }]
    })

    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res == {
        'json': {'float': 12.12, 'integer': 42},
        'list': [
            {'lastname': 'mogollon', 'name': 'johan'},
            {'lastname': 'mogollon', 'name': 'johan'},
            {'age': [12, 24], 'lastname': 'paul', 'name': 'jean'}
        ]}
    assert err == {
        'list': [
            {'list.0.age': 'Missing field'},
            {'list.1.age': 'Missing field'}
        ]
    }

    json = dumps({
        'json': {
            'integer': 42,
            'float': 12.12
        },
        'list': [42, 61, 22]
    })

    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res == {'json': {'float': 12.12, 'integer': 42}, 'list': []}
    assert err == {'list': ['Bad data type', 'Bad data type', 'Bad data type']}


def test_number_rules():
    """Test rules on fields which are numbers."""
    constrain = {
        'integer': {
            'type': int,
            'gt': -1,
            'lt': 101
        },
        'float': {
            'type': float,
            'gt': -1,
            'lt': 101
        }
    }
    json = {'integer': 101, 'float': -1.0}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert not res and err == {'integer': 'Not less than 101',
                               'float': 'Not greater than -1'}

    json = {'integer': -1, 'float': 101.0}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert not res and err == {'integer': 'Not greater than -1',
                               'float': 'Not less than 101'}


def test_regex_rule():
    """Test fields ruled by regex."""
    constrain = {
        'number': {
            'format': r'^\d+$',
        }
    }
    json = {'number': 'one hundred'}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert err == {'number': 'Invalid format'} and not res

    json = {'number': '42'}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res == {'number': '42'} and not err


def test_default_rule():
    """Test fields ruled by regex."""
    constrain = {
        'number': {
            'format': r'^\d+$',
            'default': 42
        }
    }
    json = {}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res == {'number': 42} and not err


def test_inclusion_rule():
    """Test fields ruled by inclusion in list."""
    constrain = {
        'fruit': {
            'in': ['apple', 'orange', 'pineapple']
        }
    }
    json = {'fruit': 'cherry'}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert not res and err == {'fruit': 'Invalid'}

    json = {'fruit': 'apple'}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res == {'fruit': 'apple'} and not err


def test_datetime_rule():
    """Test fields is a datetime with custom format."""
    constrain = {
        'birthdate': {
            'type': datetime,
            'dformat': '%Y-%m-%d',
        }
    }
    json = {'birthdate': '1990-12-24'}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert not err and res == {'birthdate': datetime.strptime('1990-12-24', '%Y-%m-%d')}

    json = {'birthdate': '1990-13-24'}
    res, err = JsonSchemaValidator(constrain).validate(json)
    assert not res and err == {'birthdate': 'Invalid format'}
