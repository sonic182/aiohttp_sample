"""Json schemas validator."""

from json import dumps
from app.validators.json_schemas import JsonSchemaValidator


def test_validator_needs_constrain():
    """Test validator needs constrain."""
    try:
        JsonSchemaValidator('')
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

    res, err = JsonSchemaValidator(constrain).validate(json)
    assert err
    del constrain['extra_1']
    del constrain['extra_2']

    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res and not err


def test_constrain_lists_dicts():
    """Test constrain primitive types"""
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
            'lastname': 'mogollon'
        }]
    })

    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res and not err

    json = dumps({
        'json': {
            'integer': 42,
            'float': 12.12
        },
        'list': [42, 61]
    })

    res, err = JsonSchemaValidator(constrain).validate(json)
    assert res and not err
