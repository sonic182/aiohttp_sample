"""Custom logger module."""
import logging
import collections

from app.config.settings import basepath


class MyLoggerAdapter(logging.LoggerAdapter):
    """Handle extra params for logging message."""

    def __init__(self, logger, *args):
        """Overrides."""
        if isinstance(args[0], dict):
            self.app = args[0].get('app', None)
            self.request = args[0].get('request', None)
        super(MyLoggerAdapter, self).__init__(logger, *args)

    def process(self, msg, kwargs):
        """Proccess message."""
        data, kwargs = self.setup_kwargs_data(msg, kwargs)
        return super(MyLoggerAdapter, self).process(
            self._parse_data(data), kwargs)

    def setup_kwargs_data(self, msg, kwargs=None):
        """Configure data to be logged."""
        data = kwargs.get('data', {})
        if data:
            del kwargs['data']  # param not accepted by process super.
        kwargs['extra'] = kwargs.get('extra', {})

        if self.request is not None:
            try:
                kwargs['extra']['uuid'] = self.request.uuid
            except AttributeError:
                kwargs['extra']['uuid'] = ''
        else:
            kwargs['extra']['uuid'] = ''
        kwargs['extra']['type'] = msg

        return collections.OrderedDict(sorted(data.items())), kwargs

    @staticmethod
    def _parse_data(extra, key=''):
        """Append data params recursively.

        TODO: change to secuential implementation.
        """
        res = ''
        if isinstance(extra, dict):
            for _key in extra:
                temp_key = '{}{}{}'.format(key, ('.' if key else ''), _key)
                res += MyLoggerAdapter._parse_data(extra[_key], temp_key)

        elif isinstance(extra, list):
            for ind, item in enumerate(extra):
                temp_key = '{}{}{}'.format(key, ('.' if key else ''), ind)
                res += MyLoggerAdapter._parse_data(item, temp_key)
        else:
            return res + '{}={}; '.format(key, extra)
        return res


class MyFilter(logging.Filter):
    """Custom logger filter."""

    def __init__(self, name='', **kwargs):
        """Initialize MyFilter.

        This filter allows loggers or handlers to log just a specific level.
        kwargs must have levels argument with a list of levels allowed to log.
        """
        self.levels = kwargs.get('levels', [])
        super(MyFilter, self).__init__(name)

    def filter(self, record):
        """Filter record."""
        if record.levelno in self.levels:
            return True
        return False


def get_logger(name='aiohttp_sample', logpath=basepath('logs', 'my.log'),
               info_log=None, error_log=None, loglevel=logging.DEBUG,
               debug=False):
    """Get logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)

    formatter = logging.Formatter(
        '%(asctime)s; LEVEL=%(levelname)s; uuid=%(uuid)s; type=%(type)s; '
        '%(message)s'
    )

    if info_log is None and error_log is None:
        file_handler = logging.FileHandler(logpath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    elif not (info_log and error_log):
        raise ValueError(
            'You must specify info_log and error_log if one of then retrieved')
    else:
        info_handler = logging.FileHandler(info_log)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        info_handler.addFilter(MyFilter(levels=[
            logging.INFO, logging.WARNING]))

        err_handler = logging.FileHandler(error_log)
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(formatter)
        err_handler.addFilter(MyFilter(levels=[
            logging.ERROR, logging.CRITICAL]))
        logger.addHandler(info_handler)
        logger.addHandler(err_handler)

    if debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return MyLoggerAdapter(logger, {})
