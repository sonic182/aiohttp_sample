"""My Logger tests."""

import collections
import logging
from uuid import uuid1

from app.config.logger import MyLoggerAdapter
from app.config.logger import MyFilter
from app.config.logger import get_logger

from tests.common import get_client_app


def test_get_logger():
    """Test logger retreive."""
    assert get_logger()
    assert get_logger(info_log='/tmp/info.log', error_log='/tmp/info.log')
    try:
        get_logger(info_log='/tmp/info.log')
        assert False
    except ValueError:
        assert True


def test_log_filter():
    """Test log filter."""
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.INFO)
    logger.addFilter(MyFilter(levels=[logging.INFO, logging.WARNING]))

    logger.debug('hello world')
    logger.error('hello world')
    assert True


def test_log_extras():
    """Test log extras not raise erros."""
    msg = MyLoggerAdapter._parse_extras(extra={
        'a': {
            'b': 'b',
            'c': 'c'
        },
        'd': ['e', 'f', 'g']
    })
    assert msg == 'a.b=b; a.c=c; d.0=e; d.1=f; d.2=g; '


async def test_log_uuid(test_client):
    """Test log uuid works."""
    app, client = await get_client_app(test_client)
    logger = get_logger(debug=True, logpath='/tmp/sample.log').logger

    class CustomRequest:
        uuid = str(uuid1())

    extra = {'foo': 'bar'}
    logger = MyLoggerAdapter(logger, {'app': app, 'request': CustomRequest})
    response_extra, kwargs = logger.my_extra('a message', {'extra': extra})
    assert kwargs == {'extra':
                      {'uuid': CustomRequest.uuid, 'type': 'a message'}}
    assert response_extra == collections.OrderedDict(sorted(extra.items()))
