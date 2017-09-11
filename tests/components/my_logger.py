"""My Logger tests."""

from uuid import uuid4

from app.config.logger import MyLoggerAdapter
from app.config.logger import get_logger

from tests.common import get_client_app


def test_get_logger():
    """Test logger retreive."""
    assert get_logger()


def test_log_extras():
    """Test log extras not raise erros."""
    logger = get_logger(debug=True, logpath='/tmp/sample.log')

    logger.info('a message', extra={
        'a': {
            'b': 'b',
            'c': 'c'
        },
        'd': ['e', 'f', 'g']
    })
    assert True


async def test_log_uuid(test_client):
    """Test log uuid works."""
    app, client = await get_client_app(test_client)
    logger = get_logger(debug=True, logpath='/tmp/sample.log').logger

    class CustomRequest:
        uuid = str(uuid4())

    logger = MyLoggerAdapter(logger, {'app': app, 'request': CustomRequest})
    logger.info('a message', extra={'foo': 'bar'})
    assert True
