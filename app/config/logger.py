
import logging
import collections

from app.config.settings import basepath


class MyLoggerAdapter(logging.LoggerAdapter):
    """Handle extra params for logging message."""

    def process(self, msg, extra={}, **kwargs):
        """Proccess message."""
        if isinstance(extra['extra'], dict):
            extra = extra['extra']
        extra = {
            'type': msg,
            **extra
        }
        extra = collections.OrderedDict(sorted(extra.items()))
        return self.__class__.print_extras(extra), kwargs

    @classmethod
    def print_extras(cls, extra, key=''):
        """Append extra params recursively.

        TODO: change to secuential implementation.
        """
        res = ''
        if isinstance(extra, dict):
            for _key in extra:
                temp_key = '{}{}{}'.format(key, ('.' if key else ''), _key)
                res += cls.print_extras(extra[_key], temp_key)

        elif isinstance(extra, list):
            for ind, item in enumerate(extra):
                temp_key = '{}{}{}'.format(key, ('.' if key else ''), ind)
                res += cls.print_extras(item, temp_key)
        else:
            return res + '{}={}; '.format(key, extra)
        return res


def get_logger(name='aiohttp_sample', logpath=basepath('logs', 'my.log')):
    """Get logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(logpath)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s; LEVEL=%(levelname)s; %(message)s')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return MyLoggerAdapter(logger, {})
