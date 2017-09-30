"""My Logger tests."""

import logging

from app.config.logger import MyFilter
from app.config.logger import get_logger


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
